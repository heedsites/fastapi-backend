from pydantic import BaseModel, Field
from typing import List


class TestCase(BaseModel):
    """Test case with input and expected output."""
    input: str = Field(..., description="Input for the test case")
    output: str = Field(..., description="Expected output for the test case")

    class Config:
        json_schema_extra = {
            "example": {
                "input": "5\n1 2 3 4 5",
                "output": "15"
            }
        }


class QuestionRequest(BaseModel):
    """Request model for generating a coding question."""
    topic: str = Field(..., description="Topic/subject of the coding question", example="arrays")
    difficulty: str = Field(..., description="Difficulty level", example="medium")
    language: str = Field(..., description="Programming language", example="python")

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "arrays",
                "difficulty": "medium",
                "language": "python"
            }
        }


class QuestionResponse(BaseModel):
    """Response model containing the generated coding question."""
    question: str = Field(..., description="The coding question description")
    constraints: str = Field(..., description="Constraints for the problem")
    input_format: str = Field(..., description="Format specification for input")
    output_format: str = Field(..., description="Format specification for output")
    sample_input: str = Field(..., description="Sample input example")
    sample_output: str = Field(..., description="Sample output example")
    test_cases: List[TestCase] = Field(..., description="List of test cases with input/output pairs")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Find the sum of all elements in an array",
                "constraints": "1 <= n <= 1000, -1000 <= arr[i] <= 1000",
                "input_format": "First line contains n, second line contains n space-separated integers",
                "output_format": "Print a single integer representing the sum",
                "sample_input": "5\n1 2 3 4 5",
                "sample_output": "15",
                "test_cases": [
                    {"input": "5\n1 2 3 4 5", "output": "15"},
                    {"input": "3\n10 20 30", "output": "60"}
                ]
            }
        }
