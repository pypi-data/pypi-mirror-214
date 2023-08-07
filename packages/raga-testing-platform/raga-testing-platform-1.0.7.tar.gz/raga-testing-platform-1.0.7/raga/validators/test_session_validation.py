
class TestSessionValidator:
    @staticmethod
    def validate_project_name(project_id: str) -> str:
        if not project_id:
            raise ValueError("Project name is required.")
        # Additional validation logic specific to project name
        return project_id

    @staticmethod
    def validate_project_name(project_name: str) -> int:
        if not project_name:
            raise ValueError("Project name is required.")
        # Additional validation logic specific to project id
        return project_name

    @staticmethod
    def validate_run_name(run_name: str) -> str:
        if not run_name:
            raise ValueError("Run name is required.")
        # Additional validation logic specific to run name
        return run_name


