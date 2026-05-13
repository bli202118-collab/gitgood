# README

### 打新的code之前，下載(同步)Github上的版本 Before typing any new codes, download(pull) the current version from Github
git pull origin main
### 切回主分支
git checkout main 

### 建立個人分支(以防直接修改共用內容造成版本錯誤)
git checkout -b 'nameA'
### 做出更改後確認現在狀態用(可看出哪些有修改需要add/push)
git status
### 把現有所有的更改丟入"暫存"(最後面那個點很重要! 就是代表"全部"一定要有!)
git add .
### 存入並對這次的更新內容做解釋(description填寫訊息)
git commit -m "description"
### 第一次push
git push -u origin 'nameA'
### 事後都push進nameA的話就不用後面那段
git push
