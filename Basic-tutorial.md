## 1. Downloading git

Git is the application that powers services such as Github and Gitlab. It is essential for sharing and storing code. For the rest of this tutorial you will need to have a working installation of git which can be downloaded [here](https://git-scm.com/). If you have downloaded and installed this we can get started. Do quickly verify whether git was installed correctly by typing `git --version` in the _command line interface_ (CLI) of your operating system. For MacOS, this would be terminal; for Windows, it's called command prompt. Then, press the Enter key on your keyboard. If Git was installed correctly you should get a response like "Git version 2.49.0"


## 2. Downloading Github Desktop

This application provides a nice visual interface for interacting with Github. It is highly recommended for beginners as it means you don't have to use the command line. It can be downloaded [here](https://desktop.github.com/download/). After installation it is important that you authenticate yourself. This can be done by going into settings, then accounts, and then signing into Github. If you do not have a github account yet please create one.

It is of course also possible to use the more traditional command-line interface. We recommend a visual interface for people who are unfamiliar with Git and just starting out. Should you nonetheless want to use CLI instead we recommend the following resource: [Git CLI tutorial](https://git-scm.com/book/en/v2/Getting-Started-The-Command-Line)

## 3. Creating a new repository

Your research project, including code, data and documentation, is stored in what's called a repository. It is important to note here that you will have a local repository and a remote repository. The remote one is the one that is hosted on Github and the local one only exists on your device. If you have made any changes to the project  on your device, these are now part of your local repository and by "pushing" these to the remote repository, you can update the remote repository. This way, you can share your repository with other collaborators, allowing them to not only view but also contribute to your repository. Once a collaborator has made changes to the shared project and "pushed" these from their local version of the repository, you can review, comment on, accept/reject them, and even ask for revisions. If you are happy with these changes, you can "merge" them into the remote shared repository. Then, you can "pull" these changes so that your local repository reflects the up-to-date version. 

When you're starting a new project, there are a couple of scenarios:
1. You are starting a new and blank project.
2. Somebody else has started the project already and pushed it to Github.
3. You have started the project on your device but haven't pushed it to Github.

This is how to proceed depending on the scenario

1. In this case you can simply click "New Repository" in Github Desktop.
2. In this case you have to "clone" that repository. This just means setting up the local repository based on the remote repository. If you go to the homepage of that repository on Github there should be a green button which displays a link when clicked. You should copy this link. Then you can go to Github desktop and click clone repository and paste the link. After that Github Desktop takes care of the rest of the setup.
3. In this case you can click on "Add Local Repository" after which you will have to select the folder containing your current version of the project. If this already happened to contain a .git file the rest happens automatically, if it didn't you simply click "create a repository here instead"

NOTE: Pushing to github does not necessarily publish your code so that it is visible for everyone to see. You can set your repository to private if you want to have control over who sees your code/data.

## 4. Making changes
When making changes it is important to understand two concepts, commits and branches. Let's say you have made a certain change to some code. The project is now different. What you then do is save the new version of the project by "committing" it. You can see the changes in Github Desktop and see the commit button down below with the option to add message to the new version. Once committed it is saved. You can then also "push" it so the new version is available for possible collaborators on Github. Branches much like those attached to a tree can run in parallel. Here that means that you keep multiple versions (branches) of the same project which you can edit separately. When working with other people you can each work on your own version (branch) of the project without interfering with each other's work. You can also recombine these branches if you want to merge the separate changes you and your collaborator made. You can create a new branch by clicking on "current branch" and then clicking "new branch".

## 5. When and why do I even do all of this?
### The why
The reason this workflow is important is because it allows you to share your work with others as well as making sure it is reusable and maintainable. Git makes sure others can use your work in less than thirty seconds without you even sending an email or any files. Things such as commits, branching, continuous integration (quality control), ensure you can keep track of what has been done and how. This also means you can easily revert changes. Let's say for example you added something new to your project like extra analysis for a new dataset and it seems to work okay but later you find out this change has broken a different part of your code. Now you can easily find where the problem is and roll back those changes to get back to working code.

### The when
The most basic flow is as follows
1. You have a project repository and you want to change something (anything really).
2. You create a new branch where you will change said thing.
3. You make some changes and you commit and push these. Likely this will happen multiple times as this change consists of multiple smaller changes.
4. You have changed what you wanted to change so you create a PR. 
5. You click merge.
6. You are done.

This of course leaves a couple of questions unanswered, namely:
1. I need names for these commits and branches, what do I call them?
2. What is a smaller change and can be a commit and what needs its own branch? 
3. How do I do a PR?

Which we will answer in detail below
1. It often helps to give them appropriate names. For example if you've added an extra feature be that analysis or an extra button. Now you would like to indicate that this commit/branch added an extra feature. However if you just fixed an existing problem you want the name to clearly convey that as well. This is why best practices have been developed which can be found in the Github guidelines file.
2. This is a question even seasoned developers struggle with. General advice here would be that once you start working on some change (feature/fix/chore anything really), and you are working on that branch, to only have commits that are in direct service to that change. If it is something that you encounter which is not directly linked, but you want to fix it, it is probably best to first finish the existing change and then move on to that task. This helps keep branches focussed.
3. If you or a collaborator has made changes on a branch you can start a PR on Github by going to "pull requests" and then clicking on "New pull request". In an ideal scenario no other changes have been made since you started working on a branch and you have people that are also working on the project. These people can then review the changes you've made and give an honest assessment of the quality of the code. In the case that other changes have been made you probably have merge conflicts. In this case you first need to merge main into your branch and resolve conflicts locally after which you can merge still. If there is no one to review your PR you must do this yourself. In this case be honest about the quality of the code and whether there are still improvements that need to be made before it can be merged to main.