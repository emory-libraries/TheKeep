class ContentsSubjects < ActiveRecord::Base
  belongs_to :content
  belongs_to :subject
end
