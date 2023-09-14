
# 导入sqlite3模块
import sqlite3
import re
# 读取文件stephen_king_adaptations.txt
with open("stephen_king_adaptations.txt", "r") as f:
    # 将文件内容复制到一个列表中，命名为stephen_king_adaptations_list
    stephen_king_adaptations_list = f.readlines()

# 建立一个新的SQLite数据库连接，命名为stephen_king_adaptations.db
conn = sqlite3.connect("stephen_king_adaptations.db")
# 创建一个游标对象
cur = conn.cursor()
# 创建一个表，命名为stephen_kind_adaptations_table，列名为movieID, movieName, movieYear, imdbRating
cur.execute("CREATE TABLE IF NOT EXISTS stephen_kind_adaptations_table (movieID INTEGER PRIMARY KEY, movieName TEXT, movieYear INTEGER, imdbRating REAL)")

# 将stephen_king_adaptations_list中的内容插入到表stephen_king_adaptations_table中
for line in stephen_king_adaptations_list:
    # 用逗号分割每一行，并去掉空格
    data = [x.strip() for x in line.split(",")]

    # 假设 data[0] = 'M01'
    data[0] = int(re.search(r'\d+', data[0]).group())

    # 检查 movieID 是否已经存在
    cur.execute("SELECT 1 FROM stephen_kind_adaptations_table WHERE movieID = ?", (data[0],))
    if cur.fetchone() is None:
        # 如果 movieID 不存在，插入新记录
        cur.execute("INSERT INTO stephen_kind_adaptations_table (movieID,movieName, movieYear, imdbRating) VALUES (?, ?, ?, ?)", data)
    else:
        # 如果 movieID 已经存在，更新记录（或者选择其他操作）
        cur.execute("UPDATE stephen_kind_adaptations_table SET movieName = ?, movieYear = ?, imdbRating = ? WHERE movieID = ?", (data[1], data[2], data[3], data[0]))

# 提交数据库的更改
conn.commit()

# 给用户提供在数据库中搜索电影的选项，根据以下参数。这应该在一个循环中呈现给用户，直到用户选择停止：
while True:
    print("请从以下选项中选择一项来搜索数据库中的电影：")
    print("1. 电影名称")
    print("2. 电影年份")
    print("3. 电影评分")
    print("4. 停止")

    # 获取用户输入
    choice = input("请输入你的选择：")

    # 如果用户选择选项1，那么询问用户要在数据库中搜索的电影名称
    if choice == "1":
        # 获取用户输入的电影名称
        movie_name = input("请输入电影名称：")
        # 查询数据库中的电影详情
        cur.execute("SELECT * FROM stephen_kind_adaptations_table WHERE movieName = ?", (movie_name,))
        # 获取查询结果
        result = cur.fetchone()
        # 如果找到了电影，显示该电影的所有详情，包括名称、年份和评分
        if result:
            print(f"{movie_name}的电影详情：")
            print(f"电影ID: {result[0]}")
            print(f"电影名称: {result[1]}")
            print(f"电影年份: {result[2]}")
            print(f"IMDB评分: {result[3]}")
        # 如果没有找到电影，显示一条消息
        else:
            print(f"我们的数据库中没有这部电影。")

    # 如果用户选择选项2，那么询问用户一个年份，并返回数据库中在该年份发布的所有电影详情（如上）
    elif choice == "2":
        # 获取用户输入的电影年份
        movie_year = input("请输入电影年份：")
        # 查询数据库中在该年份发布的所有电影
        cur.execute("SELECT * FROM stephen_kind_adaptations_table WHERE movieYear = ?", (movie_year,))
        # 获取所有查询结果
        results = cur.fetchall()
        # 如果找到了任何电影，显示它们的详情
        if results:
            print(f"{movie_year}年发布的电影：")
            for result in results:
                print(f"电影ID: {result[0]}")
                print(f"电影名称: {result[1]}")
                print(f"电影年份: {result[2]}")
                print(f"IMDB评分: {result[3]}")
                print("-"*20)
        # 如果没有找到任何电影，显示一条消息
        else:
            print(f"我们的数据库中没有在那一年发布的电影。")

    # 如果用户选择选项3，那么询问用户一个评分限制，只返回数据库中等于或高于该评分的电影。例如，如果用户输入5，那么只有那些IMDB评分为5或高于5的电影才会被返回
    elif choice == "3":
        # 获取用户输入的评分限制
        rating_limit = input("请输入评分限制（等于或高于该评分的电影才会被返回）：")
        # 查询数据库中所有等于或高于评分限制的电影
        cur.execute("SELECT * FROM stephen_kind_adaptations_table WHERE imdbRating >= ?", (rating_limit,))
        # 获取所有查询结果
        results = cur.fetchall()
        # 如果找到了任何电影，显示它们的详情
        if results:
            print(f"评分等于或高于{rating_limit}的电影：")
            for result in results:
                print(f"电影ID: {result[0]}")
                print(f"电影名称: {result[1]}")
                print(f"电影年份: {result[2]}")
                print(f"IMDB评分: {result[3]}")
                print("-"*20)
        # 如果没有找到任何电影，显示一条消息
        else:
            print(f"我们的数据库中没有等于或高于该评分的电影。")

    # 如果用户选择选项4，那么终止程序
    elif choice == "4":
        print("感谢你使用我们的程序。再见！")
        break

    # 如果用户输入了一个无效的选项，显示一条消息
    else:
        print("无效的选项。请再试一次。")

# 关闭游标对象
cur.close()
# 关闭数据库连接
conn.close()

