let todos = [];
const todoList = document.getElementById("todo-list");

function retrieveTodos() {
    const storedTodos = localStorage.getItem('todos');
    if (storedTodos) {
        todos.push(...JSON.parse(storedTodos));
        renderTodos();
    }
}

retrieveTodos();

function renderTodos() {
    todoList.innerHTML = "";
    todos.forEach(function(todo) {
        const li = document.createElement("li");
        
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = todo.done;
        checkbox.classList.add("checkbox");

        const label = document.createElement("span");
        label.textContent = todo.text;
        if (todo.done) {
            label.classList.add("done");
        }

        li.appendChild(checkbox);
        li.appendChild(label);

        if (todo.done) {
          const deleteButton = document.createElement("button");
          deleteButton.textContent = "delete";
          deleteButton.classList.add("deleteButton");
          deleteButton.addEventListener("click", function(event) {
            event.stopPropagation(); // Prevent the li click event from firing
            todos = todos.filter(function(item) {
              return item !== todo;
            });
            localStorage.setItem('todos', JSON.stringify(todos));
            renderTodos();
          });
          li.appendChild(deleteButton);
        }
        li.addEventListener("click", function() {
            todo.done = !todo.done;
            localStorage.setItem('todos', JSON.stringify(todos));
            renderTodos();
        });
        todoList.appendChild(li);
    });
}

document.getElementById("addButton").addEventListener("click", function(event){
  event.preventDefault();

  const todoInput = document.getElementById("todo");
  const text = todoInput.value.trim();

  if (text) {
    todos.push({text, done: false});
    todoInput.value = "";
    renderTodos();
    localStorage.setItem('todos', JSON.stringify(todos));
  }
});

document.getElementById("clearButton").addEventListener("click", function(event){
  todos = todos.filter(function(todo) {
    return !todo.done;
  });
  renderTodos();
  localStorage.setItem('todos', JSON.stringify(todos));
});
