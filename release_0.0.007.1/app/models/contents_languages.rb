class ContentsLanguages < ActiveRecord::Base
  belongs_to :content
  belongs_to :language
end
