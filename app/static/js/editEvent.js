document.addEventListener('DOMContentLoaded', function() {

    const showPopup = document.getElementById('showpopup');
    const cancelPopup = document.getElementById('cancelpopup');
    const editEventForm = document.getElementById('edit-event');
    const deleteEvent = document.getElementById('deleteEvent');

    showPopup.addEventListener('click', e => {
        e.preventDefault();
        editEventForm.style.display = 'grid';
        return;
    });
    
    
    cancelPopup.addEventListener('click', e => {
        e.preventDefault();
        editEventForm.style.display = 'none';
        return;
    });


    deleteEvent.addEventListener('click', async function(e) {
        e.preventDefault();

        const eventID = deleteEvent.getAttribute('data-eventId');

        const isConfirmed = confirm('Do you really want to delete this event ?');
        if (isConfirmed) {

            const res = await deleteEventFunction(eventID);
            alert('event sucessfully deleted');
            if (res) window.location.href = 'http://127.0.0.1:8000/dashboard/'
        }
    })

});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {    
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}


async function deleteEventFunction(eventID) {

    const res = await fetch(`/event/${eventID}/`, {
        headers: {
          'X-CSRFToken': getCookie('csrftoken') // Django CSRF token
        },
        credentials: 'include',
        method: 'delete'
      });

    const data = await res.json();

    return data;
}   