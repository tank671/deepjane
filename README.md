# deepjane

Automatic text generation in the style of Jane Austen.

The project uses the fastai library (all steps to generate the
model are in the jupyter notebook).  The model is an AWD-LSTM,
pretrained on a subset of English Wikipedia (the WikiText-103
dataset https://www.sysml.cc/doc/50.pdf) and fine-tuned on
Jane Austen's complete works, downloaded from Project Gutenberg
(http://www.gutenberg.org/ebooks/31100).

The text generator is online at https://deepjane.now.sh, and also tweets periodically at https://twitter.com/AutoAusten.
To interact with the twitter bot, tweet a few words to @AutoAusten.
