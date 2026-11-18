let todos = [];
const todoList = document.getElementById("todo-list");

fetch("/api/todos")
  .then(response => response.json())
  .then(data => {
    todos = data;
    renderTodos();
  })
  .catch(error => {
    console.error("Error fetching todos:", error);
  });

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
            fetch(`/api/todos/${todo.id}`, {
              method: "DELETE"
            })
            .then(response => {
            if(!response.ok) {
              throw new Error("Network response was not ok");
            }
            todos = todos.filter(t => t.id !== todo.id);
            renderTodos();
          })
          .catch(error => {
            console.error("Error deleting todo:", error);
          });
        });
          li.appendChild(deleteButton);
      }
      li.addEventListener("click", function() {
        todo.done = !todo.done;
        renderTodos();

        fetch(`/api/todos/${todo.id}`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({done: todo.done})
        })
        .then(response => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
        })
        .catch(error => {
          console.error("Error updating todo:", error);
        });
      });

        todoList.appendChild(li);
    });
}

document.getElementById("addButton").addEventListener("click", function(event){
  event.preventDefault();

  const todoInput = document.getElementById("todo");
  const text = todoInput.value.trim();
  if (!text) {
    return; // Don't add empty tasks
  }

  fetch ("/api/todos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({text: text})
  })
  .then(response => response.json())
  .then(newTodo => {
    todos.push(newTodo);
    todoInput.value = "";
    renderTodos();
  })
  .catch(error => {
    console.error("Error adding todo:", error);
  });

});

document.getElementById("clearButton").addEventListener("click", function(event) {
  // 1. Collect the completed tasks.
  const completed = todos.filter(todo => todo.done);

  // 2. Start one DELETE request per completed task. Each request returns a promise.
  const requests = completed.map(todo =>
    fetch(`/api/todos/${todo.id}`, { method: "DELETE" })
      .then(response => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return todo.id;
      })
  );

  // 3. Wait for all the requests, then remove the deleted tasks from the list.
  Promise.all(requests)
    .then(deletedIds => {
      todos = todos.filter(todo => !deletedIds.includes(todo.id));
      renderTodos();
    })
    .catch(error => {
      console.error("Error clearing completed todos:", error);
    });
});