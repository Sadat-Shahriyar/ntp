#!/usr/bin/env python3
"""Decompose a semantic_graph.json into one JSON package per candidate proof target.

No external dependencies. The input graph is NEVER modified. Outputs:

  OUTPUT_ROOT/<paper_id>/proof_targets.json
  OUTPUT_ROOT/<paper_id>/units/<node_id>.json

Default extraction includes all labeled theorems/lemmas/corollaries/propositions,
plus source-backed unlabeled mathematical claims (excluding worked examples and
experimental/narrative observations). Other modes allow adjusting the selection.

Dependencies are candidates for formalization, NOT certified proof prerequisites.

Usage:
  python3 decompose_proof_targets.py semantic_graph.json
  python3 decompose_proof_targets.py semantic_graph.json --output-root results
  python3 decompose_proof_targets.py semantic_graph.json --mode labeled
  python3 decompose_proof_targets.py semantic_graph.json --mode all-claims
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import json
import hashlib
from pathlib import Path
import re
import sys

# The relation direction is consistent with the agreed semantic graph schema:
# "A depends_on B" means A requires B. Never follow reverse uses/depends_on.
DEPENDENCY_RELATIONS = {"uses", "depends_on", "assumes", "derives_from", "defines"}
FORMAL_LABEL = re.compile(r"^\s*(Theorem|Lemma|Corollary|Proposition|Claim|Fact)\b", re.I)
SAFE_PAPER_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
KNOWN_TYPES = {
    "context", "entity", "parameter", "assumption", "definition", "operator",
    "criterion", "algorithm", "claim", "proof_step", "proof_obligation", "unknown"
}
EXPERIMENT_TOKENS = (
    "experiment", "empirical", "sample_count", "observed", "frequency_distribution",
    "practical_choice", "tradeoff", "worked_example", "example_", "_example",
    "recommendation"
)


def safe_unit_filename(node_id: str) -> str:
    """Keep semantic node IDs unchanged in JSON, sanitize only filesystem names."""
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", node_id):
        return f"{node_id}.json"
    readable = re.sub(r"[^A-Za-z0-9_-]+", "_", node_id).strip("_")[:50] or "node"
    digest = hashlib.sha256(node_id.encode("utf-8")).hexdigest()[:10]
    return f"{readable}_{digest}.json"


def sort_key(identifier: str):
    match = re.match(r"^([A-Za-z_-]*)(\d+)$", identifier)
    return (match.group(1), int(match.group(2))) if match else (identifier, -1)


def ordered(items):
    return sorted(set(items), key=sort_key)


def load_graph(path: Path):
    try:
        graph = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read valid UTF-8 JSON from {path}: {exc}") from exc
    if not isinstance(graph, dict) or not isinstance(graph.get("paper_id"), str):
        raise ValueError("Input must be an object with string paper_id")
    if not SAFE_PAPER_ID.fullmatch(graph["paper_id"]):
        raise ValueError("paper_id must use only letters, numbers, underscores or hyphens")
    if not isinstance(graph.get("nodes"), list) or not isinstance(graph.get("edges"), list):
        raise ValueError("Graph needs arrays named 'nodes' and 'edges'")
    nodes = {}
    for i, node in enumerate(graph["nodes"]):
        if not isinstance(node, dict) or not isinstance(node.get("id"), str):
            raise ValueError(f"Invalid node at index {i}")
        if node["id"] in nodes:
            raise ValueError(f"Duplicate node ID: {node['id']}")
        if not isinstance(node.get("type"), str):
            raise ValueError(f"Node {node['id']} lacks a type")
        if node["type"] not in KNOWN_TYPES:
            # Unknown extensions are preserved rather than silently dropped.
            pass
        nodes[node["id"]] = node
    for i, edge in enumerate(graph["edges"]):
        if not isinstance(edge, dict) or edge.get("from") not in nodes or edge.get("to") not in nodes:
            raise ValueError(f"Edge {i} refers to missing/invalid endpoint")
        if not isinstance(edge.get("relation"), str):
            raise ValueError(f"Edge {i} missing relation")
    return graph, nodes


def scope(node):
    data = node.get("scope")
    return data if isinstance(data, dict) else {}


def context_ancestors(context_id, nodes):
    """Child context first; preserve hierarchy without infinite cycles."""
    path = []
    seen = set()
    while context_id:
        if context_id in seen or context_id not in nodes:
            break
        seen.add(context_id)
        if nodes[context_id]["type"] != "context":
            break
        path.append(context_id)
        context_id = scope(nodes[context_id]).get("context_id")
    return path


def experimental_context_ids(nodes):
    """Find experiments by explicit context meaning; include their descendants."""
    experiment_roots = set()
    for node in nodes.values():
        if node["type"] != "context":
            continue
        concept = (node.get("concept") or "").lower()
        if any(x in concept for x in ("experiment", "simulation", "benchmark", "evaluation_subset")):
            experiment_roots.add(node["id"])
    return {
        node["id"] for node in nodes.values() if node["type"] == "context"
        and experiment_roots.intersection(context_ancestors(node["id"], nodes))
    }


def worked_example_groups(nodes):
    """Infer example groups using an explicitly named example entity."""
    return {
        scope(n).get("group_id") for n in nodes.values()
        if n.get("type") == "entity"
        and "example" in (n.get("concept") or "").lower()
        and scope(n).get("group_id")
    }


def select_targets(nodes, mode):
    exp_contexts = experimental_context_ids(nodes)
    example_groups = worked_example_groups(nodes)
    selected, skipped = [], []
    for n in nodes.values():
        if n["type"] not in ("claim", "proof_obligation"):
            continue
        formal = bool(FORMAL_LABEL.match(n.get("label") or ""))
        reason = None
        if mode == "labeled" and not formal:
            reason = "unlabeled_claim"
        elif mode == "mathematical" and not formal:
            concept = (n.get("concept") or "").lower()
            value = (n.get("value") or "").lower()
            context = scope(n).get("context_id")
            group = scope(n).get("group_id")
            if context in exp_contexts:
                reason = "empirical_context"
            elif group in example_groups:
                reason = "worked_example"
            elif any(token in concept for token in EXPERIMENT_TOKENS):
                reason = "narrative_or_empirical_claim"
            elif any(token in value for token in ("results shown in fig.", "results shown in fig ",
                                                   "in our experiments", "authors observed", "authors report")):
                reason = "empirical_report"
        if reason:
            skipped.append({"node_id": n["id"], "concept": n.get("concept"),
                            "label": n.get("label"), "reason": reason})
        else:
            selected.append(n)
    selected.sort(key=lambda n: sort_key(n["id"]))
    return selected, skipped


def prior_work_hint(target):
    notes = (target.get("notes") or "").lower()
    value = (target.get("value") or "").lower()
    if any(x in notes for x in ("prior result", "prior work", "attributed", "historical", "earlier published",
                                "prior source", "cited result", "referenced prior", "prior literature")) or value.startswith("attributed to"):
        return "cited_prior_work"
    return "not_determined_from_graph"


def build_unit(target, nodes, edges, outgoing, argument_for, issue_links):
    root = target["id"]
    primary_proof_steps = set(argument_for.get(root, ()))
    group = scope(target).get("group_id")
    # Graceful fallback for graphs that omitted argues_for edges.
    group_fallback = set()
    if group and not primary_proof_steps:
        group_fallback = {n["id"] for n in nodes.values() if n["type"] == "proof_step"
                          and scope(n).get("group_id") == group}
    own_steps = primary_proof_steps | group_fallback

    # Walk dependency edges from the claim AND the claim's own proof steps.
    # Do not import proof steps of prerequisite theorems: they are independent units.
    core = {root} | own_steps
    todo = deque(ordered(core))
    while todo:
        current = todo.popleft()
        for next_id in outgoing.get(current, ()):
            if nodes[next_id]["type"] == "unknown":
                continue
            if nodes[next_id]["type"] == "proof_step" and next_id not in own_steps:
                # Not a source step of this target's own proof.
                continue
            if next_id not in core:
                core.add(next_id)
                todo.append(next_id)

    # Context ancestry is inherited, not treated as proved or as theorem premise.
    context_id = scope(target).get("context_id")
    contexts = set(context_ancestors(context_id, nodes))
    for node_id in core:
        contexts.update(context_ancestors(scope(nodes[node_id]).get("context_id"), nodes))

    # Model context attributes are candidates, not automatically required hypotheses.
    ambient = {
        n["id"] for n in nodes.values()
        if n["type"] in ("entity", "parameter", "assumption")
        and scope(n).get("context_id") in contexts
        and scope(n).get("group_id") is None
    }

    # Issues are attached to core through direct graph links, or shared source
    # group with one of the target's actual dependencies; they are NOT traversed.
    issue_reasons = defaultdict(set)
    for node_id in core:
        for issue_id in issue_links.get(node_id, ()):
            issue_reasons[issue_id].add("linked_to:" + node_id)
    relevant_groups = {
        scope(nodes[node_id]).get("group_id") for node_id in core
        if nodes[node_id]["type"] in ("claim", "proof_step", "definition", "criterion", "algorithm", "operator")
    }
    relevant_groups.discard(None)
    for n in nodes.values():
        if n["type"] == "unknown" and scope(n).get("group_id") in relevant_groups:
            issue_reasons[n["id"]].add("shared_source_group")
    issues = set(issue_reasons)

    included = core | contexts | ambient | issues
    local_edges = [edge for edge in edges if edge["from"] in included and edge["to"] in included]
    claims = {id_ for id_ in core if id_ != root and nodes[id_]["type"] in ("claim", "proof_obligation")}
    direct_claim_deps = {
        node_id for node_id in outgoing.get(root, ())
        if node_id in claims
    }
    all_evidence = ordered(e for node_id in included for e in (nodes[node_id].get("evidence_ids") or []))
    category_ids = {
        name: ordered(n for n in core if nodes[n]["type"] == type_)
        for name, type_ in (
            ("claim_dependencies", "claim"), ("definition_ids", "definition"),
            ("criterion_ids", "criterion"), ("algorithm_ids", "algorithm"),
            ("operator_ids", "operator"), ("assumption_ids", "assumption"),
            ("parameter_ids", "parameter"), ("entity_ids", "entity")
        )
    }
    category_ids["claim_dependencies"] = ordered(claims)

    notes = [
        "Graph-derived links are candidate dependencies; they are not a proof or a completeness guarantee.",
        "Ambient model nodes are context candidates, not automatically theorem premises.",
        "Only this target's source proof steps are imported. Prerequisite claims have their own proof units.",
        "Issue associations require review; unresolved or conflicting source evidence is never silently repaired."
    ]
    if group_fallback:
        notes.append("Proof steps were associated by shared source group because no argues_for edge was found.")

    result = {
        "paper_id": target["paper_id"] if "paper_id" in target else None,
        "proof_unit_id": None,
        "target": {
            "node_id": root, "type": target["type"], "label": target.get("label"),
            "concept": target.get("concept"), "statement": target.get("value"),
            "expression": target.get("expression"), "status": target.get("status"),
            "context_id": scope(target).get("context_id"),
            "group_id": group, "evidence_ids": target.get("evidence_ids", []),
            "origin_hint": prior_work_hint(target),
            "prosa_verification_status": "not_evaluated"
        },
        "dependencies": {
            "direct_claim_ids": ordered(direct_claim_deps),
            "transitive_claim_ids": ordered(claims),
            **category_ids,
            "own_proof_step_ids": ordered(own_steps),
            "context_ids": ordered(contexts),
            "ambient_model_ids": ordered(ambient),
            "issue_ids": ordered(issues)
        },
        "issues": [
            {"node_id": id_, "status": nodes[id_].get("status"),
             "concept": nodes[id_].get("concept"), "description": nodes[id_].get("value"),
             "association_reasons": sorted(issue_reasons[id_])}
            for id_ in ordered(issues)
        ],
        "evidence_ids": all_evidence,
        "source_proof_available": bool(own_steps),
        "nodes": [nodes[node_id] for node_id in ordered(included)],
        "edges": local_edges,
        "extraction_notes": notes
    }
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("semantic_graph", type=Path, help="Input semantic_graph.json")
    parser.add_argument("--output-root", type=Path, default=Path("proof_targets"),
                        help="Parent output directory; paper ID subfolder is created (default proof_targets)")
    parser.add_argument("--mode", choices=["mathematical", "labeled", "all-claims"], default="mathematical",
                        help="mathematical (default): labeled + unlabeled nonempirical claims; "
                             "labeled: only named theorem/lemma/etc.; all-claims: all claim nodes")
    args = parser.parse_args(argv)
    try:
        graph, nodes = load_graph(args.semantic_graph)
        targets, skipped = select_targets(nodes, args.mode)
        if not targets:
            raise ValueError("No matching proof candidates found in graph")
        edges = graph["edges"]
        outgoing = defaultdict(set)
        argument_for = defaultdict(set)
        issue_links = defaultdict(set)
        for edge in edges:
            src, dst, relation = edge["from"], edge["to"], edge["relation"]
            if relation in DEPENDENCY_RELATIONS and nodes[src]["type"] != "unknown":
                outgoing[src].add(dst)
            if relation == "argues_for" and nodes[src]["type"] == "proof_step":
                argument_for[dst].add(src)
            if nodes[src]["type"] == "unknown" and nodes[dst]["type"] != "unknown":
                issue_links[dst].add(src)
            if nodes[dst]["type"] == "unknown" and nodes[src]["type"] != "unknown":
                issue_links[src].add(dst)
        output = args.output_root / graph["paper_id"]
        units_dir = output / "units"
        units_dir.mkdir(parents=True, exist_ok=True)
        summaries = []
        emitted = set()
        for target in targets:
            unit = build_unit(target, nodes, edges, outgoing, argument_for, issue_links)
            unit["paper_id"] = graph["paper_id"]
            unit["proof_unit_id"] = f"{graph['paper_id']}:{target['id']}"
            filename = safe_unit_filename(target["id"])
            path = units_dir / filename
            path.write_text(json.dumps(unit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            emitted.add(filename)
            summaries.append({
                "node_id": target["id"], "label": target.get("label"),
                "concept": target.get("concept"),
                "kind": "labeled_result" if FORMAL_LABEL.match(target.get("label") or "") else "unlabeled_candidate",
                "origin_hint": unit["target"]["origin_hint"],
                "unit_file": "units/" + filename,
                "direct_claim_dependencies": unit["dependencies"]["direct_claim_ids"],
                "transitive_claim_dependencies": unit["dependencies"]["transitive_claim_ids"],
                "node_count": len(unit["nodes"]),
                "own_proof_step_count": len(unit["dependencies"]["own_proof_step_ids"]),
                "issue_ids": unit["dependencies"]["issue_ids"]
            })
        # Safe reruns: remove only stale files from a previous manifest in our unit
        # directory. Never remove arbitrary files in the output folder.
        old_index = output / "proof_targets.json"
        if old_index.exists():
            try:
                previous = json.loads(old_index.read_text(encoding="utf-8"))
                if previous.get("paper_id") == graph["paper_id"]:
                    for old in previous.get("targets", []):
                        name = Path(old.get("unit_file", "")).name
                        if re.fullmatch(r"[A-Za-z0-9_-]+\.json", name) and name not in emitted:
                            (units_dir / name).unlink(missing_ok=True)
            except (OSError, ValueError, TypeError):
                pass
        manifest = {
            "paper_id": graph["paper_id"],
            "source_graph": args.semantic_graph.name,
            "selection_mode": args.mode,
            "total_graph_nodes": len(nodes),
            "total_graph_claim_nodes": sum(n["type"] == "claim" for n in nodes.values()),
            "proof_target_count": len(summaries),
            "targets": summaries,
            "excluded_claims": skipped,
            "caveat": "Candidate extraction only; source dependencies and Prosa provability are unverified."
        }
        old_index.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        # Built-in structural self-check of newly written outputs.
        for summary in summaries:
            parsed = json.loads((output / summary["unit_file"]).read_text(encoding="utf-8"))
            internal_ids = {node["id"] for node in parsed["nodes"]}
            if parsed["target"]["node_id"] not in internal_ids or any(
                edge["from"] not in internal_ids or edge["to"] not in internal_ids
                for edge in parsed["edges"]
            ):
                raise ValueError("Output structural consistency failed for " + summary["node_id"])
        print(f"Paper: {graph['paper_id']} | mode: {args.mode} | proof targets: {len(summaries)}")
        print(f"Index: {old_index}")
        print(f"Units: {units_dir}")
        for s in summaries:
            print(f"  {s['node_id']:>5} | {(s['label'] or '(unlabeled)'):<14} | "
                  f"dependencies: {len(s['transitive_claim_dependencies']):>2} claims | "
                  f"issues: {len(s['issue_ids']):>2} | {s['unit_file']}")
        print("Validation: valid JSON, unique source node IDs, resolved input/output edge endpoints")
        return 0
    except (ValueError, OSError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
