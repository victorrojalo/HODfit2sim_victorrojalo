#include <QString>
#include <QQmlFile>

int main() {
    QString str("blablabla");
    return (!QQmlFile::isLocalFile(str))? 0: 1;
}
