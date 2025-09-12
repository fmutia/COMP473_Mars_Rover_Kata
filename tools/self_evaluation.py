import os

def generate_self_evaluation(output_file="SELF_EVALUATION.md"):
    content = """# Team Self-Evaluation

This document is our self-evaluation against the grading criteria for the Mars Rover Kata project.

## Grading Criteria (Total: 9 points)

### 1. Project Structure (1 point)
- Proper project structure with `src/`, `tests/`, GitHub Actions workflow:  
**Our evaluation:** [ ] Met / [ ] Partially Met / [ ] Not Met  
**Notes:** 

### 2. Test Suite (2 points)
- Comprehensive `pytest` test coverage:  
**Our evaluation:** [ ] Met / [ ] Partially Met / [ ] Not Met  
**Notes:** 

### 3. Functional Requirements (3 points)
- Implementation of the Mars Rover Kata as described:  
**Our evaluation:** [ ] Met / [ ] Partially Met / [ ] Not Met  
**Notes:** 

### 4. Nonfunctional Requirements (2 points)
- Design principles (DRY, SoC, Dependency Injection, ADRs):  
**Our evaluation:** [ ] Met / [ ] Partially Met / [ ] Not Met  
**Notes:** 

### 5. Architecture Decision Records (1 point)
- At least one ADR documented:  
**Our evaluation:** [ ] Met / [ ] Partially Met / [ ] Not Met  
**Notes:** 

---

## Summary
- Total Points (self-assessed): X / 9
- Extra Credit (if any): 

"""
    with open(output_file, "w") as f:
        f.write(content)
    print(f"Self-evaluation template created at {os.path.abspath(output_file)}")

if __name__ == "__main__":
    generate_self_evaluation()
