const form = document.querySelector(".load-form");
const fileInput = document.querySelector(".file-input");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  const file = fileInput.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = async (event) => {
    const data = JSON.parse(event.target.result);

    // Update frontend
    board = data.board;
    player = data.player;
    move_counter = data.move_counter;
    update_game_state(board, player);

    // Send to backend
    await fetch("/load_game_state", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  };

  reader.readAsText(file);
});
