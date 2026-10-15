#include <QCoreApplication>
#include <QDBusConnection>
#include <QDBusMessage>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);

    // If at least this much works then we know the library exists and functions.
    QDBusConnection sessionBus = QDBusConnection::sessionBus();
    qDebug() << "[QtDBus Test] Checking D-Bus connection with: " << sessionBus.name();
    qDebug() << "[QtDBus Test] Last error: " << sessionBus.lastError();

    return 0;
}
