from firebase_admin.messaging import Message, Notification
Message(
    notification=Notification(title="title", body="text", image="url"),
    topic="Optional topic parameter: Whatever you want",
)
{
	"to": "dod36B2YKURvrxIgpzs7KN:APA91bHpAEysHAKS4Z8Abyvd4S0mldyoBik0otZbFFx3pkf0rvPZckykldHH_8YRUHMnsfaQY4uh7cfqbXp5B7BYCXvNwK44D7fplGDu-iX5dQfjHZ84ogiaMNLqCqUkLOdEudLOTssO",
	"notification": {
		"body": "Firebase Cloud Message Body",
		"title": "Firebase Cloud Message Title",
		"subtitle": "Firebase Cloud Message Subtitle"
	}
}