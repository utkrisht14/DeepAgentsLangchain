from fastmcp import FastMCP

# ---------------------------------------------------------
# 1. Create MCP Server
# ---------------------------------------------------------

mcp = FastMCP("Course information server")

# ---------------------------------------------------------
# 2. Expose a tool through MCP
# ---------------------------------------------------------


@mcp.tool
def get_course_detail(course_name: str) -> str:
    """
    Get the duration and fee of a training course.
    """

    courses = {
        "Python": {
            "duration": "8 weeks",
            "fee": "€400"
        },

        "Machine Learning": {
            "duration": "12 weeks",
            "fee": "€700"
        },

        "Agentic AI": {
            "duration": "6 weeks",
            "fee": "€600"
        }
    }

    course = courses.get(course_name)

    if course is None:
        return f"No course information found for {course_name}."

    return (
        f"Course: {course_name}\n"
        f"Duration: {course['duration']}\n"
        f"Fee: {course['fee']}"
    )


# ---------------------------------------------------------
# 3. Run MCP Server using STDIO
# ---------------------------------------------------------

if __name__ == "__main__":
    mcp.run()