async function chooseFile() {
    let content = await eel.getFile()();
    document.getElementById('content').value = content;
}
eel.expose(update);
function update(data, target){
    document.getElementById(target).value += `\n${data}`;
    let textarea = document.getElementById(target);
    textarea.scrollTop = textarea.scrollHeight;
}
