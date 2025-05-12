rm -f *.zip
rm -rf choirbot-main
wget https://github.com/Ensemble-Continuo/choirbot/archive/refs/heads/main.zip
unzip *zip
mv choirbot-main/* .
rm -rf choirbot-main
rm -f *.zip