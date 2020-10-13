# Day 1, Part 2 Build-Convert-Run Exercise: Upload to registry
## Build, Convert, and Run an HPC job with a Container

# Step 3: Upload to a Registry

<!--
works: singularity pull shub://tutorial.jetstream-cloud.org/tutorial-containers/numpy-pillow:latest
 when did this work? it doesn't now. Maybe due to the push command used...
works: singularity pull library://ECoulter/tutorial-containers/mymandle:latest
fails: singularity pull library://ECoulter/tutorial-containers/numpy-pillow:latest
works: singularity push -U mymandle.sif library://ECoulter/tutorial-containers/mymandle:latest
fails: singularity push -U mymandle.sif library://tutorial.jetstream-cloud.org/ECoulter/tutorial-containers/mymandle:latest
-->

We're going to share our containers via a registry, now, since in
normal practice, you won't be able to build containers on the same
host that you're submitting jobs from. This also aids the goal
of reproducible science - once your container is shared, you can share 
with collaborators (and enemies) or a community of users.

#### 3(a)
So, switch to your  brower and go to 
<https://tutorial.jetstream-cloud.org>.

Select **Login** on the top bar, and you'll be asked to authenticate
via Github (you will need to allow the application read-only access to your
GitHub profile).

#### 3(b)
Now, you'll have the ability to create "collections" of containers for other
users to access, and for yourself. This is an instance of the "SRegistry" software,
which underlies the main Singularity-Hub. 
Unlike Dockerhub, the SRegistry software organizes container images by
collection, in addition to username, so 
**click "New Collection" to create one now.**

Once you've created a collection, you're ready to upload via the Singularity client.
(Will everyone need a unique name here?!)

#### 3(c)
Register the remote:

```
$ singularity remote add --no-login TutorialSRegistry https://tutorial.jetstream-cloud.org
```

#### 3(d)
And authenticate:
```$ singularity remote login TutorialSRegistry```

Now you've got a token stored on this machine that will allow you continued access to the
registry.

#### 3(e)
Next, set that repository as your default:
```$ singularity remote use TutorialSRegistry```

(If you don't do this, be prepared for subsequent commands to fail without
adding --library https://tutorial.jetstream-cloud.org/).

#### 3(d)
Upload your container via the following, 
remembering to replace `$GITHUB_USERNAME` with your actual github username
used to authenticate to the registry and `YOUR-COLLECTION-NAME` with the name of
the collection you created earlier. **Case matters** for these names as well.
**Be sure to replace USERNAME with your current username, so you don't conflict with any other 
extant containers!**
```$ singularity push -U ex1.sif library://$GITHUB_USERNAME/$COLLECTION_NAME/$USERNAME-py3-dice:latest```
