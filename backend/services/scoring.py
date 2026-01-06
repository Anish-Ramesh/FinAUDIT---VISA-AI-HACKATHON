def calculate_scores(rule_results: dict) -> dict:
    dim_scores = {}
    
    # Group results by dimension prefix (e.g. completeness_*)
    formatted_results = {}
    
    for key, res in rule_results.items():
        dim = key.split('_')[0]
        if dim not in dim_scores:
            dim_scores[dim] = {"total_weight": 0, "passed_weight": 0}
        
        dim_scores[dim]["total_weight"] += res["weight"]
        if res["passed"]:
            dim_scores[dim]["passed_weight"] += res["weight"]
            
        formatted_results[key] = res

    # Calculate dimension scores (0-100)
    final_dim_scores = {}
    total_obtained = 0
    total_possible = 0
    
    for dim, weights in dim_scores.items():
        if weights["total_weight"] > 0:
            score = (weights["passed_weight"] / weights["total_weight"]) * 100
        else:
            score = 100
        final_dim_scores[dim] = round(score, 2)
        
        total_obtained += weights["passed_weight"]
        total_possible += weights["total_weight"]

    # Overall Compliance Score
    overall_score = (total_obtained / total_possible * 100) if total_possible > 0 else 100
    
    return {
        "overall_score": round(overall_score, 2),
        "health_score": round(overall_score, 2), # Using same for now, or define different logic
        "dimension_scores": final_dim_scores,
        "rule_results": formatted_results
    }
