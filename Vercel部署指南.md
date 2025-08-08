# Vercel ������ϸָ��

��ָ�Ͻ���ϸ������ν����ݴ�ѧ����ʵ������ƽ̨���� Vercel �ϡ�

## ? ǰ��׼��

### 1. �˺�׼��
- GitHub �˺ţ����ڴ����йܣ�
- Vercel �˺ţ������� GitHub �˺�ֱ�ӵ�¼��

### 2. ���ػ���
- Git �Ѱ�װ
- ��Ŀ������׼�����

## ? ��ϸ������

### ���� 1��׼����Ŀ�ļ�

��Ŀ�Ѿ����������±�Ҫ�������ļ���

1. **`vercel.json`** - Vercel ��������
2. **`requirements.txt`** - Python ������
3. **`api/index.py`** - Vercel ר�õ� Flask Ӧ�����
4. **`.gitignore`** - Git �����ļ�����

### ���� 2������ GitHub �ֿ�

1. **��¼ GitHub**
   - ���� [github.com](https://github.com)
   - ʹ�������˺ŵ�¼

2. **�����²ֿ�**
   - ������Ͻǵ� "+" ��ť
   - ѡ�� "New repository"
   - �ֿ����ƣ�`lzu-summer-practice`������ϲ�������ƣ�
   - ����Ϊ Public��������
   - ��Ҫ��ѡ "Initialize this repository with a README"
   - ��� "Create repository"

### ���� 3���ϴ����뵽 GitHub

����Ŀ��Ŀ¼�������У�ִ���������

```bash
# ��ʼ�� Git �ֿ�
git init

# ��������ļ�
git add .

# �ύ����
git commit -m "Initial commit: ���ݴ�ѧ����ʵ������ƽ̨"

# ���Զ�ֿ̲⣨�滻Ϊ���� GitHub �û����Ͳֿ�����
git remote add origin https://github.com/zasdcn/lzu-summer-practice.git

# ���ʹ��뵽 GitHub
git branch -M main
git push -u origin main
```

### ���� 4������ Vercel

1. **���� Vercel**
   - �� [vercel.com](https://vercel.com)
   - ��� "Sign Up" �� "Log In"
   - ѡ�� "Continue with GitHub" ʹ�� GitHub �˺ŵ�¼

2. **������Ŀ**
   - ��¼�󣬵�� "New Project"
   - �� "Import Git Repository" �����ҵ����մ����Ĳֿ�
   - ��� "Import"

3. **������Ŀ**
   - **Project Name**: ����Ĭ�ϻ��޸�Ϊ��ϲ��������
   - **Framework Preset**: ѡ�� "Other"
   - **Root Directory**: ����Ĭ�ϣ�./��
   - **Build and Output Settings**: ����Ĭ��
   - ��� "Deploy"

### ���� 5���ȴ��������

1. **�������**
   - Vercel ���Զ���� `vercel.json` ����
   - ��װ Python ����
   - ����Ӧ��
   - ����ȫ�� CDN

2. **����״̬**
   - ��ɫ���ţ�����ɹ�
   - ��ɫ��ţ�����ʧ�ܣ��鿴��־�Ų����⣩

### ���� 6������������վ

����ɹ���Vercel ���ṩ��
- **��ʱ����**: �� `your-project-name.vercel.app`
- **�Զ�������**: �����������а��Լ�������

## ? ����������

### ���� 1������ʧ��

**����ԭ��**��
- Python �汾������
- ��������װʧ��
- ����·������

**�������**��
1. ��� Vercel ������־
2. ȷ�� `requirements.txt` �еİ��汾
3. ��� `vercel.json` �����Ƿ���ȷ

### ���� 2�����ݿ�����

**ע��**��Vercel ���޷�����ƽ̨����֧�ֳ־û��� SQLite ���ݿ⡣

**�������**��
1. **����/��ʾ����**��ʹ���ڴ����ݿ⣨ÿ�����������ã�
2. **��������**������ʹ�������ݿ����
   - [PlanetScale](https://planetscale.com/)��MySQL��
   - [Supabase](https://supabase.com/)��PostgreSQL��
   - [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

### ���� 3����̬�ļ�����

**����**���ϴ���ͼƬ�޷���ʾ

**�������**��
- ʹ���ƴ洢�����簢���� OSS����Ѷ�� COS��
- ��ʹ�� Vercel �ľ�̬�ļ��й�

## ? ���²���

�����޸Ĵ����ֻ��Ҫ���͵� GitHub��

```bash
# ����޸ĵ��ļ�
git add .

# �ύ�޸�
git commit -m "���¹�������"

# ���͵� GitHub
git push
```

Vercel ���Զ���⵽�����������²���

## ? ��غͷ���

Vercel �ṩ�˷ḻ�ļ�ع��ܣ�

1. **����ͳ��**���鿴��վ������
2. **���ܼ��**��ҳ������ٶ�
3. **������־**������ʱ����׷��
4. **������ʷ**���鿴���в����¼

## ? �Ż�����

### �����Ż�
1. **���û���**���������þ�̬��Դ����
2. **ͼƬ�Ż�**��ʹ�� WebP ��ʽ��ѹ��ͼƬ��С
3. **����ָ�**��������� JavaScript

### ��ȫ�Ż�
1. **��������**��������Ϣ�洢�� Vercel ����������
2. **HTTPS**��Vercel �Զ��ṩ SSL ֤��
3. **���ʿ���**�������������뱣���� IP ������

## ? ����֧��

����������⣺

1. **�鿴�ĵ�**��[Vercel �ٷ��ĵ�](https://vercel.com/docs)
2. **����֧��**��[Vercel ����](https://github.com/vercel/vercel/discussions)
3. **��ϵ����**����Ŀ����֧������

## ? �������

��ϲ���������ݴ�ѧ����ʵ������ƽ̨�ѳɹ����� Vercel��

**��һ��**��
- ����������վ����
- ��ʼ����ʵ������
- �����Ŷӳ�Աʹ��

---

**ע������**��
- ��Ѱ� Vercel ��һ����ʹ�����ƣ���������ִ��ʱ��ȣ�
- ����������ܣ��ɿ������������Ѱ汾
- ���ڱ�����Ҫ����