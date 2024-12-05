function toggleCommentField(selectElement) {
            const commentField = document.getElementById('commentField');
            const imageFiled = document.getElementById('imageFiled');
            if (selectElement.value === 'status_2') {
                imageFiled.style.display = 'none';
                commentField.style.display = 'block';
            }else if (selectElement.value === 'status_3') {
                commentField.style.display = 'none';
                imageFiled.style.display = 'block';
            } else {
                commentField.style.display = 'none';
            }
        }

        document.addEventListener("DOMContentLoaded", function() {
            const statusSelect = document.getElementById('new_status');
            toggleCommentField(statusSelect);
        });