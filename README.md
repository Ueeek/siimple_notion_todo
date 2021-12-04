A simple Neovim remote plugin for Todo-list Management on Notion

# Setup
You have to set some environment variables before use this
```
export NOTION_TODO_TOKEN_V2=''
export NOTION_TODO_PAGE_URLL=``
```
* token v2 is auth-token which you can find it in Cokkie of notion
* PAGE_URL is the page url you use to this plugin
    * recommend to create new_page for this plugin


# Usage
```
:NotionTodoTodoList
```
* create new split window and show todo-list

```
:NotionTodoAddTodo task_name
```
* create new_entry named "task_name" in todo_list

```
:NotionTodoDeleteTodo task_idx
```
* delete {task_idx}-th entry from todo_list
* index is 0-origin

```
:NotionTodoToggleTodo task_idx
```
* toggle {done,not_done} status of {task_idx}-th entry in todo_list

# Caution
* this plugin edit notion-page
    * DO NOT SET IMPORTANT NOTION PAGE 
        * create new page for this plugin is recommended

# LIMITATION
* TodoBlockにしか対応してないので、その他のobjは無視されます
* nested Todoには対応してないです。
        
# SCREENSHOT
* notionこんな感じだと
！[notion](https://user-images.githubusercontent.com/43738558/144712750-4846657b-a3ec-46a7-84ad-6ccea36ae1f9.png)
* こんな感じで表示されて
![show list](https://user-images.githubusercontent.com/43738558/144712752-7a9009ef-3347-4945-9eca-79b458149653.png)
* Toggleでこんな感じになる
![toggle](https://user-images.githubusercontent.com/43738558/144712756-de6b101f-4ba4-40f3-a58d-baa8dc0f55c7.png)
