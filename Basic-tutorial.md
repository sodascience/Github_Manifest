## 1. Starter resources
In the rest of this tutorial we will assume some basic knowledge on how committing, pushing, and branching works. Some good resources are:
* [W3Schools](https://www.w3schools.com/git/default.asp?remote=github)
* [Webtuu](https://webtuu.com/blog/04/git-basics-branching-merging-push-to-github)
* [Rogerdudler](https://rogerdudler.github.io/git-guide/)

Please note that these tutorials are as general as possible so they use a lot of terminal commands. It is very likely that you will be working with a text editor/IDE such as Visual studio/PyCharm/others which often are integrated with github and have greatly simplified all steps. In this case take a brief look at one of the links above to get an idea of how the git system works and then look up the "(program you'll be using) + git" and you will find a very easy way to work with it.

## 2. When and why do I even do all of this?
### The why
The reason this workflow is important is because it allows you to share your work with others as well as making sure it is reusable and maintainable. Git makes sure others can use your work in less than thirty seconds without you even sending an email or any files. Things such as commits, braching, continuous integration (quality control), makes sure you can keep track of what has been done and how. This also means you can easily revert changes. Let's say for example you added something new to your project like extra analysis for a new dataset and it seems to work okay but later you find out this change has broken a different part of your code. Now you can easily find where the problem is and roll back those changes to get back to working code.

### The when
The most basic flow is as follows
1. You have a project repository and you want to change something (anything really).
2. You create a new branch where you will change said thing. (A branch is just a copy of the project)
3. You make some changes and you commit and push these. Likely this will happen multiple times as this change consists of multiple smaller changes.
4. You have changed what you wanted to change so you create a PR. 
5. You click merge.
6. You are done.

This of course leaves a couple of questions unanswered, namely:
* How do I even get a repository, do I need to create a branch to add this?
* I need names for these commits and branchese, what do I call them?
* What is a smaller change and can be a commit and what needs its own branch? 
* How do I do a PR?

Which we will answer in detail below
* You create a repository by going to github and clicking on the new icon. Once this is done you have your remote repo. That is to say the one that is published on github. Upon creating this Github gives you the option whether to push existing work to there or to simply clone the repo to your local computer. Depending on whether you already have work you should take one of these options.
* It often helps to give them appropriate names. For example if you've added an extra feature be that analysis or an extra button you would like to indicate that this commit/branch added an extra feature. However if you just fixed an existing problem you want the name to clearly convey that as well. This is why best practices have been developed which can be found in the Github guidelines file.
* This is a question even seasoned developers struggle with. General advice here would be that once you start working on some change (feature/fix/chore anything really) and you are working on that branch to only have commits that are in direct service to that change. If it is something that you encounter which is not directly linked but you want to fix it is probably best to first finish the existing change and then move on to that task. This helps keep branches focussed.
* In an ideal scenario no other changes have been made since you started working on a branch and you have people that are also working on the project and can review the changes you've made and give an honest assesment of the quality of the code. In the case that other changes have been made you probably have merge conflicts. In this case you first need to merge main into your branch and resolve conflicts locally after which you can merge still. If there is no one to review your PR you must do this yourself, in this case be honest about the quality of the code and whether there are still improvements that need to be made before it can be merged to main.