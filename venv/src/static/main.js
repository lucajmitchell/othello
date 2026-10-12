const board_el = document.querySelector(".board");
const player_el = document.querySelector(".player");

// board and player are global to allow download.js to access them
let board;
let player;

const update_game_state = (newBoard, newPlayer) => {
  board = newBoard;
  player = newPlayer;

  player_el.innerHTML = `Current Player: ${player}`;
  board_el.innerHTML = "";

  for (let row = 0; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      const cell = document.createElement("div");
      cell.classList.add("cell");
      cell.dataset.row = row;
      cell.dataset.col = col;

      if (board[row][col] === "Dark ") {
        const disc = document.createElement("div");
        disc.classList.add("disc", "dark");
        cell.appendChild(disc);
      }

      if (board[row][col] === "Light") {
        const disc = document.createElement("div");
        disc.classList.add("disc", "light");
        cell.appendChild(disc);
      }

      board_el.appendChild(cell);
    }
  }

  // Handling AI's turn
  if (player === "Light") {
    fetch("/get_ai_move", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ board: board }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "game over") {
          alert(
            `Game Over! Winner: ${data.winner}. Dark: ${data.dark_count}, Light: ${data.light_count}`
          );
        }

        fetch("/make_move", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ row: data.row, col: data.col }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "game over") {
              alert(
                `Game Over! Winner: ${data.winner}. Dark: ${data.dark_count}, Light: ${data.light_count}`
              );
            }

            if (data.status === "success") {
              update_game_state(data.board, data.next_player);
            }
          });
      });
  }

  // Handling human's turn
  document.querySelectorAll(".cell").forEach((cell) => {
    cell.addEventListener("click", () => {
      const row = cell.dataset.row;
      const col = cell.dataset.col;
      console.log(`Cell clicked at row ${row}, col ${col}`);

      fetch("/make_move", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ row: row, col: col }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "game over") {
            alert(
              `Game Over! Winner: ${data.winner}. Dark: ${data.dark_count}, Light: ${data.light_count}`
            );
          }

          if (data.status === "success") {
            update_game_state(data.board, data.next_player);
          }

          if (data.status === "invalid move") {
            alert("Illegal move! Try again.");
          }
        });
    });
  });
};

initial_board = [
  ["None ", "None ", "None ", "None ", "None ", "None ", "None ", "None "],
  ["None ", "None ", "None ", "None ", "None ", "None ", "None ", "None "],
  ["None ", "None ", "None ", "None ", "None ", "None ", "None ", "None "],
  ["None ", "None ", "None ", "Light", "Dark ", "None ", "None ", "None "],
  ["None ", "None ", "None ", "Dark ", "Light", "None ", "None ", "None "],
  ["None ", "None ", "None ", "None ", "None ", "None ", "None ", "None "],
  ["None ", "None ", "None ", "None ", "None ", "None ", "None ", "None "],
  ["None ", "None ", "None ", "None ", "None ", "None ", "None ", "None "],
];

document.addEventListener("DOMContentLoaded", () => {
  update_game_state(initial_board, "Dark ");
});
