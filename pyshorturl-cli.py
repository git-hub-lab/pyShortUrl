
from optparse import OptionParser
import os
import sys

try:
    from ShortUrl.base_shortner import ShortnerServiceError
    from ShortUrl.goo_gl import Googl
    from ShortUrl.bit_ly import Bitly
    from ShortUrl.conf import SUPPORTED_SERVICES
except ImportError:
    print 'pyShortUrl is not installed.'
    sys.exit(-1)

if '__main__' == __name__:

    parser = OptionParser()
    parser.add_option("-r", "--service", dest="service",
                      help="One of the shortening services %s. Defaults to goo.gl" \
                          %','.join((SUPPORTED_SERVICES)))

    parser.add_option("-u", "--login", dest="login",
                      help="The user account to use with the url shortening service.")

    parser.add_option("-l", "--long-url", dest="long_url",
                      help="Shorten the specified URL.")

    parser.add_option("-k", "--api-key", dest="svc_api_key",
                      help="Use API Key while communicating with the url shortening service.")

    parser.add_option("-s", "--short-url", dest="short_url",
                      help="Expand the specified Short URL.")

    parser.add_option("-q", "--qr-code-file", dest="qr_img_path",
                      help="Used with -s. Writes the qr code for the corresponding short url.")

    (options, args) = parser.parse_args()

    # Validate the service that the user specified. If nothing is specified, we
    # default to goo.gl
    if options.service:
        if options.service not in SUPPORTED_SERVICES:
            print 'Unsupported service %s. Supported services are %s.' \
                %(options.service, ', '.join(SUPPORTED_SERVICES))
            sys.exit(-1)
    else:
        options.service = 'goo.gl'

    # Now, instantiate the service object based upon user preference.
    service = None
    if 'goo.gl' == options.service:
        service = Googl(options.svc_api_key)
    elif 'bit.ly' == options.service:
        # bit.ly requires a login account and api key.
        if not options.login or not options.svc_api_key:
            print 'bit.ly requires a valid account and API key.'
            sys.exit(-1)
        service = Bitly(options.login, options.svc_api_key)

    # Get QR code.
    if options.qr_img_path:
        if not options.short_url:
            print 'You need to specify a short url to get qr code.'
            print 'Usage: python %s -s <short_url> -q <image_path>' %(sys.argv[0])
            sys.exit(-1)

        try:
            service.write_qr_image(options.short_url, options.qr_img_path)
        except ShortnerServiceError, e:
            print e

        if os.path.exists(options.qr_img_path):
            print 'Wrote the qr code for %s to %s' %(options.short_url, options.qr_img_path)
        sys.exit(0)

    # Shorten a URL.
    if options.long_url:
        try:
            short_url = service.shorten_url(options.long_url)
            print short_url
        except ShortnerServiceError, e:
            print e
        sys.exit(0)

    # Expand a short url.
    if options.short_url:
        try:
            long_url = service.expand_url(options.short_url)
            print long_url
        except ShortnerServiceError, e:
            print e
        sys.exit(0)

