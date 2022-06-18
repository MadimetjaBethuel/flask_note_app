

function deleteNote(noteId) {

   /* 
   Acess the delete fucntion from flask and deletes the note with the id noteId
   
   */

    fetch("/delete-note",{
        method: "POST",
        body: JSON.stringify ({
            noteId: noteId
        }),
    }).then((_res) => {
        window.location.href ="/";
        }
    );}