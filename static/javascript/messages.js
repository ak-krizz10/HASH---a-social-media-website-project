let input_message = $('#input_message')
let message_body = $('.chatbox')
let send_message_form = $('#send-message-form')
const USER_ID = $('#logged-in-user').val()
let loc = window.location
let wsStart = 'ws://'


if(loc.protocol === 'https:'){
    let wsStart = 'wss://'
}
let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function(e){
    console.log('open', e)
    send_message_form.on('submit', function (e) {
        e.preventDefault()
        let message = input_message.val()
        let send_to = get_active_other_user_id()
        let thread_id = get_active_thread_id()
        let data = {
            'message' : message,
            'sent_by' : USER_ID,
            'send_to' : send_to,
            'thread_id' : thread_id
        } 
        data = JSON.stringify(data)
        socket.send(data)
        $(this)[0].reset()
    })
}

socket.onmessage = async function(e){
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    newMessage(message, sent_by_id, thread_id)
}

socket.onerror = async function(e){
    console.log('error', e)
}

socket.onclose = async function(e){
    console.log('close', e)
}

function newMessage(message, sent_by_id, thread_id){
    if($.trim(message) === ''){
        return false;
    }
    var today = new Date();
    var time = today.getHours() + ":" + today.getMinutes();
    let message_element;
    let chat_id = 'chat_' + thread_id
    if(sent_by_id ==USER_ID){
        if( message.includes('http:')|| message.includes('https:')){
            message_element = `
            <div class="message my_message">
                <p>
                    <a href="${message}">${message}</a>
                    <br><span>${time}</span>
                </p>
            </div>`
        }else{
            message_element = `
            <div class="message my_message">
                <p>
                    ${message}<br>
                    <span>${time}</span>
                </p>
            </div>`
        }
    }
    else{
        if( message.includes('http:')|| message.includes('https:')){
            message_element = `
            <div class="message frnd_message">
                <p>
                    <a href="${message}">${message}</a>
                    <br><span>${time}</span>
                </p>
            </div>`
        }else{
            message_element = `
            <div class="message frnd_message">
                <p>
                    ${message}<br>
                    <span>${time}</span>
                </p>
            </div>`
        }
    }
    
    let message_body = $('.right-side[chat-id="' + chat_id + '"] .chatbox')
    message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
    input_message.val(null);
}

$('.chat-block').on('click', function(){
    $(' .chat-block.active').removeClass('active')
    $(this).addClass('active')

    //message wrapper a.k.a right-side
    let chat_id = $(this).attr('chat-id')
    $('.right-side.now_active').removeClass('now_active')
    $('.right-side[chat-id="' + chat_id +'"]').addClass('now_active')
})


function get_active_other_user_id(){
    let other_user_id = $('.right-side.now_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id(){
    let chat_id = $('.right-side.now_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}