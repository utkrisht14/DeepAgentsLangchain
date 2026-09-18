from fastmcp import FastMCP

# ---------------------------------------------------------
# Create MCP Server
# ---------------------------------------------------------

mcp = FastMCP("Course information server")

# ---------------------------------------------------------
# MCP Tool
# ---------------------------------------------------------

@mcp.tool()
def get_course_details(course_name: str) -> str:
    """
    Get the duration and fee of a course.
    """

    courses = {
        "Python": {
            "duration": "8 weeks",
            "fee": 400
        },

        "Machine Learning": {
            "duration": "12 weeks",
            "fee": 700
        },

        "Agentic AI": {
            "duration": "6 weeks",
            "fee": 600
        }
    }

    course = courses.get(course_name)

    if course is None:
        return f"No course information found for {course_name}."

    return (
        f"Course: {course_name}\n"
        f"Duration: {course['duration']}\n"
        f"Fee: €{course['fee']}"
    )


# ---------------------------------------------------------
# Start MCP Server
# ---------------------------------------------------------

if __name__ == "__main__":
    mcp.run()