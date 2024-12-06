from subject_predictor import predict_subject

text = '''
The Ontological Argument for God An ontological argument for God was proposed by the Italian philosopher, monk, and Archbishop of
Canterbury Anselm 10331109. Anselm lived in a time where belief in a deity was often assumed. He, as a
person and as a prior of an abbey, had experienced and witnessed doubt. To assuage this doubt, Anselm
endeavored to prove the existence of God in such an irrefutable way that even the staunchest of nonbelievers
would be forced, by reason, to admit the existence of a God.
Anselms proof is a priori and does not appeal to empirical or sense data as its basis. Much like a proof in
geometry, Anselm is working from a set of givens to a set of demonstrable concepts. Anselm begins by
defining the most central term in his argumentGod. For the purpose of this argument, Anselm suggests, let
God  a being than which nothing greater can be conceived. He makes two key points
1
'''
best_subject, scores = predict_subject(text)