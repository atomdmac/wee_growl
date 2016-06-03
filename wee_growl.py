import weechat
from growl import Registration, Notification, GROWL_UDP_PORT
from socket import socket, AF_INET, SOCK_DGRAM

# Growl notifications
addr = ("localhost", GROWL_UDP_PORT)
s = socket(AF_INET, SOCK_DGRAM)
p = Registration()
p.add_notification()
s.sendto(p.payload(), addr)

def notify(title="WeeChat", message=""):
	# Send notification to STDOUT
	# print message
	
	# Send Growl notification
	p = Notification(title=title, description=message)
	s.sendto(p.payload(), addr)

weechat.register("atom_growl", "atommac", "0.2", "GPL", "atom_growl: Growl notifications for Weechat by Atom", "", "")

# Hook privmsg/hilights
weechat.hook_signal("weechat_pv", "notify_show_priv", "")
weechat.hook_signal("weechat_highlight", "notify_show_hi", "")

# Functions
def notify_show_hi( data, signal, message ):
    """Sends highlight message to be printed on notification"""
    notify("Weechat",  message)
    return weechat.WEECHAT_RC_OK

def notify_show_priv( data, signal, message ):
    """Sends private message to be printed on notification"""
    
    # Separate username from message
    parts = message.split('\t')
    message = parts[0] + ': ' + parts[1]
    
    # HACK! If this message is from me, don't notify.
    if parts[0].strip() == 'atommac': return weechat.WEECHAT_RC_OK

    notify(title="Weechat Private Message",  message=message)
    return weechat.WEECHAT_RC_OK
