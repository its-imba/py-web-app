function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function editNote(noteId, noteData) {
  // Set the current note data in the textarea
  const updatedNoteElement = document.getElementById('note');
  if (updatedNoteElement) {
    updatedNoteElement.value = noteData;
  }

  // Set the note ID in a hidden input field
  const noteIdElement = document.getElementById('note-id');
  if (noteIdElement) {
    noteIdElement.value = noteId;
  }

  // Show the edit form
  const editFormElement = document.getElementById('edit-form');
  if (editFormElement) {
    editFormElement.style.display = 'block';
  }
}

document.addEventListener('DOMContentLoaded', function() {
  // Add event listener to the edit buttons
  const editButtons = document.querySelectorAll('.edit-button');
  editButtons.forEach(function(button) {
    button.addEventListener('click', function() {
      const noteId = button.getAttribute('data-note-id');
      const noteData = button.getAttribute('data-note-data');
      editNote(noteId, noteData);
    });
  });
});

function submitEdit() {
  const updatedNote = document.getElementById('note').value;
  const noteId = parseInt(document.getElementById('note-id').value);

  fetch(`/edit-note/${noteId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ updatedNote: updatedNote }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message === 'Note updated') {
        // Show the success message
        document.getElementById('success-message').style.display = 'block';
      }
    })
    .catch((error) => {
      console.error('Error updating note:', error);
    });
}