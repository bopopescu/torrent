from bcoding import bencode, bdecode
import hashlib
from urllib import parse
import socket
import struct, binascii, random
from hurry.filesize import size


class TorrentParser:

    def __init__(self, file_name):
        self.file = file_name

    def run(self):
        data = self.parse_file()

        announce = data['announce']
        info_hash = data['info_hash']
        parsed_url = parse.urlparse(announce)

        # if parsed_url.scheme == 'udp':
        #     request, transaction_id = self.udp_create_connection_request()
        #     data['info'] = self.scrape_udp(parsed_url, info_hash, request, transaction_id)
        # todo: should do http
        # if parsed_url.scheme in ["http", "https"]:
        #     if not announce:
        #         raise RuntimeError("%s doesnt support scrape" % data)
        #     parsed = urlparse(tracker.replace("announce", "scrape"))
        #     return scrape_http(parsed, hashes)
        return data

    @staticmethod
    def make_size(full_size):
        return size(full_size)

    def parse_file(self):
        with open(self.file, 'rb') as file:
            content = bdecode(file)

        info = content['info']
        files = []
        full_size = 0
        for file in info['files']:
            file_info = {
                'size': file['length'],
                'name': file['path'][0]
            }
            files.append(file_info)
            full_size += file['length']
        tracker_list = []
        for tracker in content['announce-list']:
            tracker_list.append(tracker[0])
        info_hash = hashlib.sha1(bencode(info)).hexdigest()
        announce_url = content['announce']
        data = {
            'info_hash': info_hash,
            'files': files,
            'announce': announce_url,
            'full_size': self.make_size(full_size),
            'tracker_list': tracker_list
        }
        return data

    def udp_create_connection_request(self):
        connection_id = 0x41727101980  # default connection id
        action = 0x0  # action (0 = give me a new connection id)
        transaction_id = int(random.randrange(0, 255))
        buf = struct.pack("!q", connection_id)  # first 8 bytes is connection id
        buf += struct.pack("!i", action)  # next 4 bytes is action
        buf += struct.pack("!i", transaction_id)  # next 4 bytes is transaction id
        return buf, transaction_id

    def scrape_udp(self, parsed_url, info_hash, request, transaction_id):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(4)
        conn = (socket.gethostbyname(parsed_url.hostname), parsed_url.port)

        sock.sendto(request, conn)
        buffer = sock.recvfrom(2048)[0]
        connection_id = self.udp_parse_connection_response(buffer, transaction_id)
        request, transaction_id = self.udp_create_scrape_request(connection_id, info_hash)

        sock.sendto(request, conn)
        buffer = sock.recvfrom(2048)[0]

        return self.udp_parse_scrape_response(buffer, transaction_id)

    def udp_parse_connection_response(self, buf, sent_transaction_id):

        if len(buf) < 16:
            raise RuntimeError("Wrong response length getting connection id: %s" % len(buf))
        action = struct.unpack_from("!i", buf)[0]   # first 4 bytes is action

        res_transaction_id = struct.unpack_from("!i", buf, 4)[0]     # next 4 bytes is transaction id
        if res_transaction_id != sent_transaction_id:
            raise RuntimeError("Transaction ID doesnt match in connection response! Expected %s, got %s"
                % (sent_transaction_id, res_transaction_id))

        if action == 0x0:
            connection_id = struct.unpack_from("!q", buf, 8)[0]     # unpack 8 bytes from byte 8, should be the connection_id
            return connection_id
        # elif action == 0x3:
        else:
            error = struct.unpack_from("!s", buf, 8)
            raise RuntimeError("Error while trying to get a connection response: %s" % error)

    def udp_create_scrape_request(self, connection_id, hash):
        action = 0x2  # action (2 = scrape)
        transaction_id = int(random.randrange(0, 255))
        buf = struct.pack("!q", connection_id)  # first 8 bytes is connection id
        buf += struct.pack("!i", action)  # next 4 bytes is action
        buf += struct.pack("!i", transaction_id)  # followed by 4 byte transaction id
        # from here on, there is a list of info_hashes. They are packed as char[]
        hex_repr = binascii.a2b_hex(hash)
        buf += struct.pack("!20s", hex_repr)
        return buf, transaction_id

    def udp_parse_scrape_response(self, buf, sent_transaction_id):
        if len(buf) < 16:
            raise RuntimeError("Wrong response length while scraping: %s" % len(buf))
        action = struct.unpack_from("!i", buf)[0]   # first 4 bytes is action

        res_transaction_id = struct.unpack_from("!i", buf, 4)[0]    # next 4 bytes is transaction id
        if res_transaction_id != sent_transaction_id:
            raise RuntimeError("Transaction ID doesnt match in scrape response! Expected %s, got %s"
                % (sent_transaction_id, res_transaction_id))

        if action == 0x2:
            ret = {}
            offset = 8  # next 4 bytes after action is transaction_id, so data doesnt start till byte 8
            ret['seeds'] = struct.unpack_from("!i", buf, offset)[0]
            offset += 4
            ret['complete'] = struct.unpack_from("!i", buf, offset)[0]
            offset += 4
            ret['leeches'] = struct.unpack_from("!i", buf, offset)[0]
            offset += 4
            return ret
        # elif action == 0x3:
        else:
            # an error occured, try and extract the error string
            error = struct.unpack_from("!s", buf, 8)
            raise RuntimeError("Error while scraping: %s" % error)

if __name__ == '__main__':
    file = '4BDEB1B31028BAD95EC6258B1FF4350EC24889A5_0zkZciY.torrent'
    parser = TorrentParser(file)

    data = parser.run()
    print(data)
