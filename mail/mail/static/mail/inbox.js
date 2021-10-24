function display_alert(alert) {
    const div = document.createElement("div");
    div.className = "alert alert-danger";
    div.innerText = alert;

    document.querySelector("#alert").appendChild(div);
}

function resetCursor(txtElement) {
    if (txtElement.setSelectionRange) {
        txtElement.focus();
        txtElement.setSelectionRange(0, 0);
    } else if (txtElement.createTextRange) {
        var range = txtElement.createTextRange();
        range.moveStart('character', 0);
        range.select();
    }
}

document.addEventListener('DOMContentLoaded', function () {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', () => {
        compose_email();
    });

    document.querySelector('#compose-form').addEventListener("submit", (e) => {
        e.preventDefault();

        const recipients = document.querySelector("input[name='recipients']").value;
        const subject = document.querySelector("input[name='subject']").value;
        const body = document.querySelector("textarea[name='body']").value;

        fetch("/emails", {
            method: "POST",
            body: JSON.stringify({
                recipients: recipients,
                subject: subject,
                body: body
            })
        }).then(response => response.json())
            .then(result => {
                if (result.error) {
                    display_alert(result.error);
                } else {
                    load_mailbox("inbox");
                }
            })
    })

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email(email) {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    document.querySelector('#email-details-view').style.display = 'none';

    console.log(email)
    console.log("hello")

    // Set default completion fields.
    if (email) {
        document.querySelector('#compose-recipients').value = `${email.sender}`;
        document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
        document.querySelector('#compose-body').value = `\nOn ${email.timestamp} ${email.sender} wrote: \n${email.body}`;
        resetCursor(document.querySelector('#compose-body'));
    } else {
        document.querySelector('#compose-recipients').value = "";
        document.querySelector('#compose-subject').value = "";
        document.querySelector('#compose-body').value = "";
    }
}

function display_email(id, sender, subject, timestamp, read) {
    const email = document.createElement("div")
    email.id = id;
    email.classList.add("row");
    email.classList.add("email");

    if (read) {
        console.log("Mark as read");
        email.classList.add("read");
    }

    const sender_text = document.createElement("div");
    sender_text.className = "col-sm";
    sender_text.innerText = sender;

    const subject_text = document.createElement("div");
    subject_text.className = "col-sm";
    subject_text.innerText = subject;

    const timestamp_text = document.createElement("div");
    timestamp_text.className = "col-sm";
    timestamp_text.innerText = timestamp;

    email.appendChild(sender_text);
    email.appendChild(subject_text);
    email.appendChild(timestamp_text);

    document.querySelector("#emails-view").appendChild(email);
}

function load_email_details(id) {
    // Hide all elements except email details div
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-details-view').style.display = 'block';

    // Reset div contents
    document.querySelector('#email-details-view').innerHTML = '';

    console.log("Mark as read");
    // Mark email as read
    fetch(`emails/${id}`, {
        method: "PUT",
        body: JSON.stringify({
            read: true,
        })
    });

    // Get email details
    fetch(`emails/${id}`)
        .then(response => response.json())
        .then(email => {
            const header = document.createElement("div");

            const hr_open = document.createElement("hr");
            header.appendChild(hr_open);

            const from = document.createElement("div");
            from.innerHTML = `<b>From: </b>${email.sender}`;
            header.appendChild(from);

            const to = document.createElement("div");
            to.innerHTML = `<b>To: </b>${email.recipients}`;
            header.appendChild(to);

            const subject = document.createElement("div");
            subject.innerHTML = `<b>Subject: </b>${email.subject}`;
            header.appendChild(subject);

            const timestamp = document.createElement("div");
            timestamp.innerHTML = `<b>Timestamp: </b>${email.timestamp}`;
            header.appendChild(timestamp);

            const reply_btn = document.createElement("button");
            reply_btn.className = "btn btn-outline-primary d-inline";
            reply_btn.innerText = "Reply";
            reply_btn.addEventListener("click", () => {
                compose_email(email)
            })
            header.appendChild(reply_btn);

            const archive_btn = document.createElement("button");
            archive_btn.className = "btn btn-outline-secondary d-inline";
            header.appendChild(archive_btn);
            if (!email.archived) {
                archive_btn.innerText = "Archive";
                archive_btn.addEventListener("click", () => {
                    fetch(`/emails/${email.id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            archived: true
                        })
                    }).then(res => {
                        load_mailbox("inbox");
                    })
                });
            } else {
                archive_btn.innerText = "Unarchive";
                archive_btn.addEventListener("click", () => {
                    fetch(`/emails/${email.id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            archived: false
                        })
                    }).then(res => {
                        load_mailbox("inbox");
                    })
                })
            }


            const hr_close = document.createElement("hr");
            header.appendChild(hr_close);

            document.querySelector("#email-details-view").appendChild(header);

            const body = document.createElement("p");
            document.querySelector("#email-details-view").appendChild(body);
            body.innerText = email.body;
        })
}

function load_mailbox(mailbox) {
    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-details-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
            for (let email of emails) {
                const sender = email.sender;
                const subject = email.subject;
                const timestamp = email.timestamp;

                display_email(email.id, sender, subject, timestamp, email.read);
            }

            const email_divs = document.querySelectorAll(".email");

            email_divs.forEach(email => {
                email.addEventListener("click", e => {
                    load_email_details(email.id);
                })
            });
        })
}