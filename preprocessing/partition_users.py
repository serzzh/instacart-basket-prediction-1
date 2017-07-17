import tensorflow as tf
import argparse
import random
from insta_pb2 import User

def random_traintest_split(records, prefix, test_frac=.05):
  train = tf.python_io.TFRecordWriter('{}train.tfrecords'.format(prefix))
  test = tf.python_io.TFRecordWriter('{}test.tfrecords'.format(prefix))
  ntrain = ntest = 0
  for record in records:
    if random.random() < test_frac:
      test.write(record)
      ntest += 1
    else:
      train.write(record)
      ntrain += 1
  print "Wrote {} records to train file and {} to test".format(ntrain, ntest)
  train.close()
  test.close()

def save_testusers(records):
  """Save the kaggle-defined test set users to their own tfrecords file."""
  out = tf.python_io.TFRecordWriter('ktest.tfrecords')
  n = 0
  for record in records:
    user = User()
    user.ParseFromString(record)
    if user.test:
      out.write(record)
      n += 1
  print "Wrote {} records to ktest.tfrecords".format(n)
  out.close()



def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-r', '--record-file', default='users.tfrecords')
  parser.add_argument('--frac', type=float, default=.05, help='Test fraction (default=.05)')
  parser.add_argument('--prefix', default='', help='Prefix for generated train/test tfrecords files')
  args = parser.parse_args()

  record_iterator = tf.python_io.tf_record_iterator(args.record_file)

  assert False, "uncomment one of the below modes"
  #random_traintest_split(record_iterator, args.prefix, args.frac)
  #save_testusers(record_iterator)

main()