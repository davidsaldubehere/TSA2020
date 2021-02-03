async function chooseFile() {
    let content = await eel.getFile()(); //awaits the back-end response for selection
    document.getElementById('content').value = content;
}
eel.expose(update);
function update(data, target){
    document.getElementById(target).value += `\n${data}`;
    let textarea = document.getElementById(target);
    //automatically scrolls down
    textarea.scrollTop = textarea.scrollHeight;
}
