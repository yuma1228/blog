import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Comment

# ユーザーを作成
print("Creating users...")
users = []
user1, created = User.objects.get_or_create(
    username='testuser1',
    defaults={'email': 'user1@example.com'}
)
if created:
    user1.set_password('password123')
    user1.save()
users.append(user1)

user2, created = User.objects.get_or_create(
    username='testuser2',
    defaults={'email': 'user2@example.com'}
)
if created:
    user2.set_password('password123')
    user2.save()
users.append(user2)

user3, created = User.objects.get_or_create(
    username='testuser3',
    defaults={'email': 'user3@example.com'}
)
if created:
    user3.set_password('password123')
    user3.save()
users.append(user3)

print(f"Created/found {len(users)} users")

# 投稿を作成
print("\nCreating posts...")
posts_data = [
    {
        'title': 'Djangoの基本を学ぼう',
        'content': 'Djangoは強力なPythonのWebフレームワークです。モデル、ビュー、テンプレートの3つの主要なコンポーネントで構成されています。',
        'author': user1
    },
    {
        'title': 'Pythonでできること',
        'content': 'Pythonは多用途なプログラミング言語です。Web開発、データ分析、機械学習など、様々な分野で使用されています。',
        'author': user1
    },
    {
        'title': 'ブログアプリの作り方',
        'content': 'ブログアプリを作るには、まずモデルを定義し、ビューを作成し、テンプレートをデザインします。認証機能も重要です。',
        'author': user2
    },
    {
        'title': 'Webデザインのコツ',
        'content': 'レスポンシブデザインを心がけ、ユーザビリティを重視しましょう。CSSフレームワークを使うと効率的です。',
        'author': user2
    },
    {
        'title': 'データベース設計のベストプラクティス',
        'content': '正規化を適切に行い、インデックスを効果的に使用することで、パフォーマンスの高いデータベースを設計できます。',
        'author': user3
    },
]

posts = []
for post_data in posts_data:
    post, created = Post.objects.get_or_create(
        title=post_data['title'],
        defaults={
            'content': post_data['content'],
            'author': post_data['author']
        }
    )
    posts.append(post)
    if created:
        print(f"  Created: {post.title}")
    else:
        print(f"  Already exists: {post.title}")

# コメントを作成
print("\nCreating comments...")
comments_data = [
    {
        'post': posts[0],
        'author': user2,
        'content': 'とても分かりやすい説明ですね！'
    },
    {
        'post': posts[0],
        'author': user3,
        'content': 'Djangoを始めたばかりですが、参考になりました。'
    },
    {
        'post': posts[1],
        'author': user2,
        'content': 'Pythonは本当に便利ですよね。'
    },
    {
        'post': posts[2],
        'author': user1,
        'content': '認証機能の実装で困っていたので助かります！'
    },
    {
        'post': posts[2],
        'author': user3,
        'content': '次はコメント機能を追加してみます。'
    },
    {
        'post': posts[3],
        'author': user1,
        'content': 'CSSフレームワークはBootstrapがおすすめですか？'
    },
    {
        'post': posts[4],
        'author': user1,
        'content': 'データベース設計は難しいですが、重要ですね。'
    },
]

comment_count = 0
for comment_data in comments_data:
    comment = Comment.objects.create(
        post=comment_data['post'],
        author=comment_data['author'],
        content=comment_data['content']
    )
    comment_count += 1

print(f"  Created {comment_count} comments")

print("\n✓ Test data creation completed!")
print(f"  Users: {User.objects.count()}")
print(f"  Posts: {Post.objects.count()}")
print(f"  Comments: {Comment.objects.count()}")
