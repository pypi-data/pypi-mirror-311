
import dashi
import numpy

def test_slice_1d():
    bins = [numpy.logspace(3, 8, 51), [-1, 10], numpy.linspace(-1, 1, 21)]
    h = dashi.histogram.histogram(3, bins, labels=['foo', 'bar', 'baz'])
    h.fill(([2e3, 1e6], [1,1], [1,1]))
    
    assert(h.stats.weightsum == 2)
    
    sel = (slice(10,None), slice(None), slice(None))
    hsub = h[sel]
    
    assert(len(hsub._h_binedges[0]) == len(h._h_binedges[0]) - (sel[0].start-1))
    assert(hsub.stats.weightsum == 1)
    assert(hsub.labels == h.labels)
    
    # re-assigning the slice produces the same result
    empty = h.empty_like()
    empty[sel] = hsub
    hsub_new = empty[sel]
    assert((hsub_new._h_bincontent == hsub._h_bincontent).all())
    
    # Check that labels are copied
    sel = (1, slice(None), slice(None))
    assert(h[sel].labels == h.labels[1:])
    
    sel = (1, 1, slice(None))
    assert(h[sel].labels == [h.labels[2]])
    

def test_slice_normalization():
    bins = [numpy.logspace(3, 8, 51), [-1, 10], numpy.linspace(-1, 1, 21)]
    h = dashi.histogram.histogram(3, bins)
    
    sel = (slice(2,-11), slice(None), slice(None))
    # put a value in the last bin
    h.fill(([1e7-1], [1], [1]))
    
    hsub = h[sel]
    # both edges and bin selection are correct
    assert(hsub._h_binedges[0][-2] == h._h_binedges[0][-12])
    assert(hsub._h_bincontent.sum(axis=(1,2))[-1] == 0)
    assert(hsub._h_bincontent.sum(axis=(1,2))[-2] == 1)
    
    # cut out last bin => value should disappear
    sel = (slice(2,-12), slice(None), slice(None))
    hsub = h[sel]
    assert(hsub.stats.weightsum == 0)