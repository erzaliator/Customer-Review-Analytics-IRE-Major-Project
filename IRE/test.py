import sys

print "started"

f = open("asd", "w")
f.write(sys.argv[1])
f.close()
print "ended"
