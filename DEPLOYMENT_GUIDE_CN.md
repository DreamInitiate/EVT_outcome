# GitHub + Streamlit Community Cloud 开源部署指南

本文件夹已经按 Streamlit Community Cloud 的标准结构准备完成。建议仓库名：
`evt-outcome-calculator`。正式公开前不要加入任何患者级数据、带身份信息的
表格、病历截图或未经期刊许可的排版版论文 PDF。

## 一、在 GitHub 建立公开仓库

1. 登录 [GitHub](https://github.com/)，点击右上角 **New repository**。
2. Repository name 填写 `evt-outcome-calculator`。
3. Description 建议填写：
   `Externally validated 3-day post-EVT calculator for 90-day unfavorable functional outcome.`
4. 选择 **Public**。
5. 不要让 GitHub 额外生成 README、许可证或 `.gitignore`，因为本文件夹已包含。
6. 创建后，把本文件夹内的全部内容上传到仓库根目录。根目录应直接看到
   `streamlit_app.py`、`requirements.txt`、`README.md` 和 `model/`。

网页上传适合首次操作：在空仓库页面点击 **uploading an existing file**，把本文件夹
内的文件和文件夹拖入上传区域，然后提交。若网页不能完整上传隐藏目录
`.streamlit` 和 `.github`，可使用 GitHub Desktop 或文末命令行方式。

## 二、替换占位信息

上传前或上传后，搜索仓库中的 `TO-BE-UPDATED`，替换以下内容：

- `README.md` 中的 GitHub 用户名、仓库地址和 Streamlit 地址；
- `CITATION.cff` 中的仓库地址、网页地址、作者和发布日期；
- 论文正式发表后补充文章 DOI 和完整引用。

如果作者顺序、通信作者或 DOI 尚未最终确定，保留占位内容比猜测更安全。

## 三、部署到 Streamlit Community Cloud

1. 打开 [share.streamlit.io](https://share.streamlit.io/) 并使用 GitHub 登录。
2. 首次使用时授权 Streamlit 读取您的公开 GitHub 仓库。
3. 点击右上角 **Create app**，选择 **Yup, I have an app**。
4. 填写：
   - Repository：`您的GitHub用户名/evt-outcome-calculator`
   - Branch：`main`
   - Main file path：`streamlit_app.py`
   - App URL：可尝试 `evt-outcome-calculator`，若已被占用可加作者缩写。
5. 打开 **Advanced settings**，Python version 选择 **3.12**。
6. 本项目不需要 Secrets，不要填写患者数据、口令或密钥。
7. 点击 **Deploy**。成功后会得到 `https://自定义名称.streamlit.app/`。

以后只要向 GitHub 的 `main` 分支提交更新，Community Cloud 通常会自动重新部署。

## 四、上线后核验

至少使用下面三组固定示例逐一核验：

| 示例 | Age | CRP | Lymphocyte | Neutrophil | NIHSS | END | Edema | 预期概率 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 70 | 10 | 1.5 | 7.5 | 15 | 0 | 0 | 0.4762971870 |
| 2 | 80 | 50 | 0.8 | 12 | 22 | 1 | 1 | 0.9635341289 |
| 3 | 55 | 3 | 2.2 | 5 | 8 | 0 | 0 | 0.2590995005 |

检查桌面端和手机端显示；确认单位为 `mg/L` 和 `×10⁹/L`；确认 END 和脑水肿
均为 No=0、Yes=1；确认网页没有宣称 0.50 是临床决策阈值。

## 五、冻结论文对应版本

1. 在 GitHub 打开 **Releases → Draft a new release**。
2. Tag 填写 `v1.0.0`，Release title 填写
   `EVT Outcome Calculator v1.0.0 — locked manuscript model`。
3. 在说明中记录论文版本、模型版本和验证测试均已通过。
4. 论文接收且作者信息完整后，可把公开仓库连接到 Zenodo，为该冻结版本生成 DOI。
5. 把 DOI 回填到 `CITATION.cff`、README 和论文 Code availability。

## 六、论文 Code availability 建议文本

> The full fixed-coefficient model specification, source code, verification
> examples, and web calculator are openly available at [GitHub repository URL].
> The web application is available at [Streamlit app URL]. The archived software
> version corresponding to this article is available at [software DOI]. The
> application does not include a patient database or application-level analytics;
> users should enter only the seven required deidentified predictor values.

## 七、命令行上传方式（可选）

在本文件夹打开终端并执行：

```bash
git init
git add .
git commit -m "Release Streamlit EVT outcome calculator v1.0.0"
git branch -M main
git remote add origin https://github.com/您的用户名/evt-outcome-calculator.git
git push -u origin main
```

如果 GitHub 要求身份验证，请使用 GitHub Desktop、浏览器登录或 GitHub 提供的
个人访问令牌；不要把密码或令牌写进代码和仓库。
