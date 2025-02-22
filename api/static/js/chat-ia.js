// Função para manter o scroll no final
function scrollToBottom() {
  const chatList = document.getElementById("chatList");
  chatList.scrollTop = chatList.scrollHeight;
}

// Modelo de mensagem da IA
function createIaMessage(reply) {
  return `
      <div class="d-flex align-items-start justify-content-between gap-16 border-bottom border-neutral-200 pb-16 mb-16">
        <div class="d-flex align-items-center gap-16">
          <div class="img overflow-hidden flex-shrink-0 sidebar-logo border-0">
            <img src="/static/images/logo.png" alt="site logo" class="light-logo w-44-px h-44-px ">
            <img src="/static/images/logo-light.png" alt="site logo" class="dark-logo w-44-px h-44-px ">
            <img src="/static/images/logo-icon.png" alt="site logo" class="logo-icon w-44-px h-44-px ">
          </div>
          <div class="info flex-grow-1">
            <h6 class="text-lg mb-4">IA</h6>
            <p class="mb-0 text-secondary-light text-sm">${reply}</p>
          </div>
        </div>
      </div>
    `;
}

// Modelo de mensagem do Usuário
function createUserMessage(message) {
  return `
      <div class="d-flex align-items-start justify-content-between gap-16 border-bottom border-neutral-200 pb-16 mb-16">
        <div class="d-flex align-items-center gap-16">
          <div class="img overflow-hidden flex-shrink-0 sidebar-logo border-0">
            <iconify-icon icon="solar:user-bold-duotone" class="w-44-px h-44-px" style="font-size: 54px;"></iconify-icon>
          </div>
          <div class="info flex-grow-1">
            <h6 class="text-lg mb-4">Usuário</h6>
            <p class="mb-0 text-secondary-light">${message}</p>
          </div>
        </div>
      </div>
    `;
}

document.getElementById("chatForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const input = document.getElementById("chatMessage");
  const apikey = document.getElementById("apikey").value;
  const message = input.value.trim();
  if (!message) return;
  input.value = "";

  // Insere a mensagem do usuário no chat
  const chatList = document.getElementById("chatList");
  chatList.insertAdjacentHTML('beforeend', createUserMessage(message));
  scrollToBottom();

  // Envia a mensagem para o backend via AJAX
  try {
    const response = await fetch("/send_message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, apikey }),
    });
    const data = await response.json();

    // Insere a resposta da IA no chat
    chatList.insertAdjacentHTML('beforeend', createIaMessage(data.reply));
    scrollToBottom();
  } catch (error) {
    console.error("Erro:", error);
  }
});