async function chooseFile() {

    let content = await eel.getFile()();
    document.getElementById('content').innerHTML = content;
}
eel.expose(update);
function update(data, target){
    document.getElementById(target).innerHTML += `\n${data}`;
    let textarea = document.getElementById(target);
    textarea.scrollTop = textarea.scrollHeight;
}
