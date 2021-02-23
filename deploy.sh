cmt="fix"
if [ -n "$1" ]; then
  cmt="$1"
fi
python3 build/build.py

cd mygitbook || exit
gitbook build . book
cd ..
git add .
git commit -m "$cmt"
git push origin main
