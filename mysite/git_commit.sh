

find . -name *.pyc | xargs rm

unset SSH_ASKPASS

git add *

git commit -m "change something"

git push






