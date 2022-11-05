import dpkt
import socket
import pygeoip
import simplekml

gi = pygeoip.GeoIP('GeoLiteCity.dat')
def main():
    f = open('wire.pcap', 'rb')
    fw= open('opkml.txt','w')
    kml = simplekml.Kml()

    pcap = dpkt.pcap.Reader(f)
    kmlheader = '<?xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
    '<Style id="transBluePoly">' \
                '<LineStyle>' \
                '<width>1.5</width>' \
                '<color>501400E6</color>' \
                '</LineStyle>' \
                '</Style>'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+plotIPs(pcap,kml)+kmlfooter
    fw.write(kmldoc)
    fw.close()

    kml.save('places.kml')
    # print(kmldoc)

def plotIPs(pcap,kml):
    kmlPts = ''
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            print(type(ip),type(eth))
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = retKML(dst, src,kml)
            kmlPts = kmlPts + KML
        except:
            pass
    return kmlPts

def retKML(dstip, srcip,kml):
    dst = gi.record_by_name(dstip)
    src = gi.record_by_name('14.139.187.110')
    try:
        dstlongitude = dst['longitude']
        dstlatitude = dst['latitude']
        srclongitude = src['longitude']
        srclatitude = src['latitude']
        kml = (
            '<Placemark>\n'
            '<name>%s</name>\n'
            '<extrude>1</extrude>\n'
            '<tessellate>1</tessellate>\n'
            '<styleUrl>#transBluePoly</styleUrl>\n'
            '<LineString>\n'
            '<coordinates>%6f,%6f\n%6f,%6f</coordinates>\n'
            '</LineString>\n'
            '</Placemark>\n'
        )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
        return kml
    except:
        return ''

if __name__ == '__main__':
    main()