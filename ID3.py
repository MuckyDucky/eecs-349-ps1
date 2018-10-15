from node import Node
import math

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  gain, question = find_best_split(examples) #TOdo : examples is a dictionary

  if gain == 0:
    return Leaf(examples)

  true_rows, false_rows = partition(examples,question)

  true_branch = ID3(false_rows)
  false_branch = ID3(false_rows)

  return Node(question,true_branch,false_branch)



def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''

  #base case
  if isinstance(node, Leaf):
    return node.predictions

  if node.question.match(example):
    return evaluate(example,node.true_branch)
  else:
    return evaluate(example,node.false_branch)

def class_counts(dataset):
  # returns dictionary that contains total count of each attribute
  counts = {}
  for row in dataset:
      label = row['Class']
      if label not in counts:
        counts[label] = 1
      else:
        counts[label] +=1
  return counts

def attr_count(dataset):
  count=0
  for attr in dataset:
    if attr!='Class':
      count += 1
  return count

def extract_attr(row):
  thelist = []
  for attr in row:
    if attr!='Class':
      thelist.append(attr)
  return thelist

def calc_entropy(rows):
  counts = class_counts(rows)
  entropy=0
  for label in counts:
    prob_lbl = counts[label]/float(len(rows))
    entropy += -prob_lbl * math.log(prob_lbl,2) #Todo : is log base 2 right?
  return entropy

def partition(rows, question): #returns tuple
  true_rows, false_rows = [], []
  for row in rows:
    if question.match(row):
      true_rows.append(row)
    else:
      false_rows.append(row)
  print("True rows : " + str(true_rows))
  print("False rows : " + str(false_rows))

  return true_rows, false_rows

def IG(left, right, current_uncertainty):
  p=float(len(left)) / (len(left)+len(right))
  #print ("IG print test : " + str((1-p)*calc_entropy(right)))
  #return (calc_entropy(right))
  return current_uncertainty - (p*calc_entropy(left) + (1-p)*(calc_entropy(right)))

def find_best_split(rows):
  best_gain = 0
  best_question = None
  current_uncertainty = calc_entropy(rows)
  n_attributes = attr_count(rows)
  #n_features = len(rows[0]) -1 #number of columns
  #Todo: need to fix to find 'Class' Key, not index number of column label

  # for col in range(n_features):
  #   values = set([list(row.values())[col] for row in rows]) #unique values in column
  #   print("column no." +str(col) +' values : ' + str(values))
  #
  for attribute in extract_attr(rows[0]):

    values = set([row[attribute] for row in rows])  # unique values in the column

    for val in values:
      question = Question(attribute,val) #(attribute, value) = (1,1)
      true_rows, false_rows = partition(rows,question)

      if len(true_rows) == 0 or len(false_rows) == 0: #if no split happens
        continue
      gain = IG(true_rows, false_rows, current_uncertainty)

      if gain >= best_gain:
        best_gain, best_question = gain, question

  return best_gain, best_question

class Question:
	def __init__(self,column,value):
		self.column = column
		self.value = value
	def match(self,example):
		val = example[self.column]
		return val == self.value
	#def __repr__(self):
	#	return "Is %s %s?" %(header[self.column], str(self.value))

class Leaf:
  def __init__(self,rows):
    self.predictions = class_counts(rows)



