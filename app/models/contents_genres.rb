class ContentsGenres < ActiveRecord::Base
  belongs_to :content
  belongs_to :genre
  
  validates_numericality_of :fieldnames
end
