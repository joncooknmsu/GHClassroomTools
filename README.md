## GHClassroomTools

Tools and info for effectively using GitHub Classroom (and other Git repos). See header comments in scripts for usage.

__getrepos.py__ is a script that will fetch all student repos, as specified by a simple CSV file.

__ghgetrepos.py__ is a script that will fetch all student repos, as specified by a CSV file that is the format of the GitHub Classroom download files (you can download an assignment's "grade" file as CSV).

__userstats.py__ is a script that generates user statistics of a repo (used to help evaluate contributions from student team members).

__pullgitrepos.py__ is a generic script that walks directories and pulls any Git repos it finds (and SVN repos if requested), just so that you don't have to manually.

__usefulshellops.txt__ is a file containing examples of some shell loops that I use right from the command line.

### GitHub Classroom Usage

I use GitHub Classroom (GHC) in two different ways, depending on course.

In CS 271, I use it "as intended", with a unique GHC assignment for each assignment or lab that the students do. In this model, students clone an assignment repo, work on it, commit and push their solution, and then don't really use the repo anymore. This is easy and simple for lower division students, but does not encourage really using a repo as it is intended, with multiple commits, and pushes and pulls. Of course they could commit and push multiple times, and pull and work from different computers, but they usually do not. 

In upper division courses (CS 370, 371, 581), I create only one individual "assignment" in GitHub, I call it something like "cs371-fa2023-individual", and then use this repo for __all__ of the individual assignments. Each assignment is done inside its own directory (folder) within the repo. This gives students a single repo that they have to use over the semester, and means they will need to do pushes and pulls to use it, especially over multiple computers (e.g., CS lab and personal). 

In both models I (or TAs) place a "grade.txt" file in the repo (and directory) for each assignment, with the first line being "Grade: ##" and then the following lines being short descriptions of any points that were deducted. We then commit and push that so that it is part of the repo. In CS 271 the students rarely become accustomed to pulling this and seeing, they just wait for Canvas.

In CS 371 and CS 581, I also create a single team project assignment, and then this becomes the team's project repo. You can designate an assignment as a team assignment, but AFAIK the students have to accept the assignment and then select a team, you can't control it. The first student to accept has to create the team.

For project teams I use the _userstats.py_ script to generate user statistics about how the team is using the repo. It is not perfect, it only captures contribution that has been merged into the main branch. It does also capture stats from the Wiki repository, which I make the students do there documentation on. Individual team members can have different "usernames" in the stats, because editing online (e.g., in the Wiki) ends up being a different "user" than a commit+push does. Indeed I've seen up to three different usernames for a single team member.

