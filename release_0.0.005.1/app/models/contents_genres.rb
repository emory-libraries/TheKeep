class ContentsGenres < ActiveRecord::Base
  belongs_to :content
  belongs_to :genre
end
