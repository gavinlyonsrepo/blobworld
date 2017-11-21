# Maintainer: gavin lyons <glyons66@hotmail.com>
# https://github.com/gavinlyonsrepo/blobworld
pkgname=blobworld
pkgver=1.1
pkgrel=2
pkgdesc="Automated pygame of a blob world written in python "
depends=()
arch=('any')
url="https://github.com/gavinlyonsrepo/blobworld"
license=('GPL')
optdepends=('numpy' 'pygame')
source=("https://github.com/gavinlyonsrepo/blobworld/archive/$pkgver.tar.gz")

md5sums=('73f0d525a51922b0275351c53de88e6e')

package() {
    cd "$srcdir/blobworld-${pkgver}"
    python setup.py install --prefix=/usr --root="$pkgdir"
    
    #readme
    install -D -m644 README.md "$pkgdir/usr/share/doc/${pkgname}/Readme.md"
}

