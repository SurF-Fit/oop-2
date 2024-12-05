function toggleCommentField(selectElement) {
            const commentField = document.getElementById('commentField');
            if (selectElement.value === 'status_2') {
                commentField.style.display = 'block';
            } else {
                commentField.style.display = 'none';
            }
        }

        document.addEventListener("DOMContentLoaded", function() {
            const statusSelect = document.getElementById('new_status');
            toggleCommentField(statusSelect);
        });