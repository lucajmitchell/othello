const download = async () => {

  // Create URL for downloading current game state
  const response = await fetch("/get_game_state");
  const data = await response.json();
  const blob = new Blob([JSON.stringify(data, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);

  // Create a temporary link to trigger download
  const a = document.createElement("a");
  a.href = url;
  a.download = "game_state.json";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
};
