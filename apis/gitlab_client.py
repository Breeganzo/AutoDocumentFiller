import gitlab
import os

class GitLabClient:
    def __init__(self, url, token):
        self.gl = gitlab.Gitlab(url, private_token=token)

    def create_branch(self, project_id, branch_name, ref='main'):
        project = self.gl.projects.get(project_id)
        try:
            # Try to get the branch first
            return project.branches.get(branch_name)
        except gitlab.exceptions.GitlabGetError:
            # Branch doesn't exist, create it
            return project.branches.create({'branch': branch_name, 'ref': ref})

    def commit_file(self, project_id, branch_name, file_path, content, commit_message):
        project = self.gl.projects.get(project_id)
        try:
            file = project.files.get(file_path, ref=branch_name)
            file.content = content
            file.save(branch=branch_name, commit_message=commit_message)
        except gitlab.exceptions.GitlabGetError:
            project.files.create({
                    'file_path': file_path,
                    'branch': branch_name,
                    'content': content,
                    'commit_message': commit_message,
            })
    
    def create_merge_request(self, project_id, source_branch, target_branch='main', title=None, description=None):
        project = self.gl.projects.get(project_id)
        try:
            # Try to create new merge request
            mr = project.mergerequests.create({
                'source_branch': source_branch,
                'target_branch': target_branch,
                'title': title,
                'description': description,
            })
            return mr
        except gitlab.exceptions.GitlabCreateError as e:
            if "Another open merge request already exists" in str(e):
                # Find and return the existing merge request
                mrs = project.mergerequests.list(state='opened', source_branch=source_branch)
                if mrs:
                    existing_mr = mrs[0]
                    if description:  # Update description if provided
                        existing_mr.description = description
                        existing_mr.save()
                    return existing_mr
            raise  # Re-raise the exception if it's not about existing MR
