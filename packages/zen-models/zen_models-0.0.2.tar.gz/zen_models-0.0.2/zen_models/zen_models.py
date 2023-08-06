from sqlalchemy import CHAR, Column, Date, DateTime, Float, ForeignKey, LargeBinary, String, TIMESTAMP, Text, \
    text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, MEDIUMTEXT, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

'''
    This is first version of package to be used as common models
'''


class Language(Base):
    __tablename__ = 'language'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))
    code = Column(String(45))
    inactive = Column(TINYINT(1), server_default=text("'0'"))


class Account(Base):
    __tablename__ = 'account'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45), nullable=False, unique=True)
    created_time = Column(DateTime)
    address = Column(String(45))
    inactive = Column(TINYINT(1), server_default=text("'0'"))
    canEmbedVideos = Column(TINYINT(1), server_default=text("'0'"))
    brandName = Column(INTEGER(11), index=True)
    coach_id = Column(ForeignKey('user.id'), index=True)
    uniqid = Column(String(255))
    video_approval = Column(TINYINT(1), server_default=text("'3'"), comment='1=Required, 2=Preferred, 3=Not Required')
    approval = Column(TINYINT(1), server_default=text("'3'"), comment='1=Required, 2=Preferred, 3=Not Required')
    featured_story = Column(INTEGER(11))
    enable_screencast = Column(String(25), nullable=False, server_default=text("'user'"))

    tag_collection = relationship('TagCollection')
    coach = relationship('User', primaryjoin='Account.coach_id == User.id')


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(255))
    title = Column(String(127))
    firstName = Column(String(255))
    lastName = Column(String(255))
    email = Column(String(255), unique=True)
    secondary_email = Column(String(255))
    defaultEmail = Column(TINYINT(1), comment='1= email, 2=secondary')
    password = Column(String(255))
    image = Column(LargeBinary)
    account_id = Column(ForeignKey('account.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    last_login_time = Column(DateTime)
    created_time = Column(DateTime)
    inactive = Column(TINYINT(1), server_default=text("'0'"))
    inactive_datetime = Column(DateTime)
    language_id = Column(ForeignKey('language.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    signature = Column(Text)
    coach_id = Column(ForeignKey('user.id'), index=True)
    secondary_coach_id = Column(ForeignKey('user.id'), index=True)
    timezone_offset = Column(Float)
    timezone = Column(INTEGER(11))
    brand_id = Column(INTEGER(11))
    terms_accepted_datetime = Column(TIMESTAMP)
    passwordchanged_time = Column(TIMESTAMP)
    otp = Column(String(255))
    thumbnail = Column(String(255))
    jwt_access_token = Column(String(255))
    jwt_refresh_token = Column(String(255))
    previous_password = Column(Text)

    account = relationship('Account', primaryjoin='User.account_id == Account.id')
    coach = relationship('User', remote_side=[id], primaryjoin='User.coach_id == User.id')
    language = relationship('Language')
    secondary_coach = relationship('User', remote_side=[id], primaryjoin='User.secondary_coach_id == User.id')
    AuthAssignment = relationship('AuthAssignment')
    user_tag_mappings = relationship('UserTagMapping')
    tag = relationship('Tag')
    tag_collection = relationship('TagCollection')


class Category(Base):
    __tablename__ = 'category'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(127), nullable=False)
    inactive = Column(TINYINT(1), server_default=text("'0'"))


class Story(Base):
    __tablename__ = 'story'

    id = Column(INTEGER(11), primary_key=True)
    title = Column(String(75), nullable=False)
    summary = Column(LONGTEXT)
    guide_id = Column(ForeignKey('video.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    owner_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    categoryID = Column(ForeignKey('category.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    inactive = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    created_time = Column(DateTime)
    background = Column(LONGTEXT)
    description = Column(LONGTEXT)
    isPrivate = Column(TINYINT(1), server_default=text("'1'"))
    story_type = Column(INTEGER(11), server_default=text("'1'"), comment='1 = Video, 2 = ScreenShare, 3 = Audio')
    approvalpreferred = Column(TINYINT(4), server_default=text("'0'"))
    purpose = Column(String(255))
    timing = Column(String(255))
    distribution = Column(String(255))
    promotedToTeam = Column(TINYINT(1), server_default=text("'0'"))
    recording = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='0 = Standard, 1 = Interactive')
    difficulty = Column(TINYINT(1), nullable=False, server_default=text("'0'"),
                        comment='0 = General, 1= Low/Easy, 2= Medium, 3 = Hard/High')
    interactive_pattern = Column(TINYINT(1), nullable=False, server_default=text("'2'"),
                                 comment='0 = General, 1 = Inbound, 2 = Outbound')
    compliance = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='0-No , 1- Yes')
    ai_version = Column(TINYINT(4))
    rule_engine = Column(String(255), server_default=text("'1.0'"), comment='Default is 1.0 and new is 1.1')
    coaching = Column(VARCHAR(255), server_default=text("'1.0'"))

    category = relationship('Category')
    # guide = relationship('Video', primaryjoin='Story.guide_id == Video.id')
    owner = relationship('User')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(INTEGER(11), primary_key=True)
    video_id = Column(ForeignKey('video.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    sender_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    recipient_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    cc_list = Column(Text)
    message = Column(LONGTEXT, nullable=False)
    inactive = Column(TINYINT(1))
    is_private = Column(TINYINT(1), server_default=text("'0'"),
                        comment='whether the comment can be seen by sender and receiver only')
    created_time = Column(DateTime)
    isSent = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    parentComment = Column(ForeignKey('comments.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    updated_time = Column(DateTime)

    parent = relationship('Comment', remote_side=[id])
    recipient = relationship('User', primaryjoin='Comment.recipient_id == User.id')
    sender = relationship('User', primaryjoin='Comment.sender_id == User.id')
    video = relationship('Video')


class Rating(Base):
    __tablename__ = 'rating'

    id = Column(INTEGER(11), primary_key=True)
    video_id = Column(ForeignKey('video.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    sharedBy = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True,
                      comment='Video Shared By')
    sharedWith = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True,
                        comment='Video Share With')
    weight = Column(TINYINT(1), nullable=False, comment='Star Rating from 1 to 5')
    created_time = Column(DateTime)

    user = relationship('User', primaryjoin='Rating.sharedBy == User.id')
    user1 = relationship('User', primaryjoin='Rating.sharedWith == User.id')
    video = relationship('Video')


class Link(Base):
    __tablename__ = 'links'

    id = Column(INTEGER(11), primary_key=True)
    owner_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    link = Column(Text, nullable=False)
    created_time = Column(DateTime)
    inactive = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    tinyURL = Column(String(127))
    link_text = Column(String(255))

    owner = relationship('User')
    story = relationship('Story')


class Resource(Base):
    __tablename__ = 'resources'

    id = Column(INTEGER(11), primary_key=True)
    actualFileName = Column(String(1023), nullable=False)
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    owner_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    path = Column(String(128), nullable=False, index=True)
    created_time = Column(DateTime)
    inactive = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    resource_text = Column(String(255))

    owner = relationship('User')
    story = relationship('Story')


class Note(Base):
    __tablename__ = 'notes'

    id = Column(INTEGER(11), primary_key=True)
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    owner_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    message = Column(LONGTEXT)

    owner = relationship('User')
    story = relationship('Story')


class Video(Base):
    __tablename__ = 'video'

    id = Column(INTEGER(11), primary_key=True)
    title = Column(LONGTEXT)
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    owner_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    path = Column(LONGTEXT)
    created_time = Column(DateTime)
    submit_user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    best_practice_answer = Column(LONGTEXT)
    best_practice = Column(TINYINT(1))
    approved = Column(TINYINT(1), server_default=text("'0'"))
    description = Column(LONGTEXT)
    isFavorite = Column(TINYINT(1), server_default=text("'0'"))
    imagePath = Column(LONGTEXT)
    videoTime = Column(BIGINT(20))
    practiceNumber = Column(INTEGER(11), server_default=text("'0'"))
    inactive = Column(TINYINT(1), server_default=text("'0'"))
    isConverted = Column(TINYINT(1), server_default=text("'1'"))
    isTelephony = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    status = Column(TINYINT(1), server_default=text("'1'"), comment='0 = cooking, 1=ready')
    domainNumber = Column(TINYINT(4), server_default=text("'0'"),
                          comment='0= nothing(default), 1 = sharperax, 2 = foundry, 3 = zenarate')
    video_type = Column(INTEGER(11), server_default=text("'1'"),
                        comment='1 = Practise, 2 = ScreenCast, 3 = Uploads, 4 = AudioOnly, 5 = InteractiveAudio')
    uploaded = Column(INTEGER(11), server_default=text("'0'"), comment='1= uploaded, 0=not uploaded')

    owner = relationship('User', primaryjoin='Video.owner_id == User.id')
    story = relationship('Story', primaryjoin='Video.story_id == Story.id')
    submit_user = relationship('User', primaryjoin='Video.submit_user_id == User.id')
    share = relationship('Share')


class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column(INTEGER(11), primary_key=True, comment='Assignment Primary Key')
    name = Column(String(255), nullable=False, comment='Assignment Name')
    inactive = Column(TINYINT(1), server_default=text("'0'"), comment='0=Active, 1=Inactive')
    descriptionValue = Column(String(255))
    due_date = Column(Date, nullable=False, comment='Due Date of Assignment')
    enable_surveys = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    coaching_due_date_gmt = Column(DateTime, comment='Due date of coaching')
    coaching_due_date = Column(String(255), comment='Due date of coaching')
    notify_time = Column(String(255), server_default=text("'0000-00-00 00:00 AM'"), comment='Time to send Mail')
    notify_time_gmt = Column(DateTime)
    timezone = Column(String(16), comment='selected timezone')
    owner_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True,
                      comment='Owner Id')
    owner_account_id = Column(ForeignKey('account.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                              index=True, comment='Owner Account Id')
    created_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='Created Time')
    assignment_type = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='1 = Practice, 2= View')
    flagPostProcess = Column(TINYINT(1), server_default=text("'0'"),
                             comment='0=Not processed, 1=processed, 2=under processing')
    flagNotifyCoaches = Column(TINYINT(1), server_default=text("'1'"), comment='0=no 1=yes 2=newlyadded')

    owner_account = relationship('Account')
    owner = relationship('User')


class AssignmentUserStoryMapping(Base):
    __tablename__ = 'assignment_user_story_mappings'

    id = Column(INTEGER(11), primary_key=True, comment='Primary Key')
    assignment_id = Column(ForeignKey('assignments.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                           index=True, comment='Assignment Id')
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True,
                      comment='Story Id')
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True,
                     comment='User Id')
    has_read = Column(TINYINT(1), server_default=text("'0'"), comment='0=Unread, 1=Read')
    has_completed = Column(TINYINT(1), server_default=text("'0'"))
    updated_time = Column(DateTime)
    created_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='Created Time')
    flagPostProcess = Column(TINYINT(1), server_default=text("'0'"),
                             comment='0=Not processed, 1=processed, 2=under processing')
    flagNotifyCoaches = Column(TINYINT(1), server_default=text("'1'"), comment='0=no 1=yes')

    assignment = relationship('Assignment')
    story = relationship('Story')
    user = relationship('User')


class Topic(Base):
    __tablename__ = 'topic'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(75), nullable=False)
    description = Column(String(255))
    inactive = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    owner_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    created_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    isPrivate = Column(TINYINT(1), server_default=text("'1'"))
    type = Column(INTEGER(11), nullable=False, server_default=text("2"), comment='1= Random, 2 = Sequential')

    owner = relationship('User')


class Section(Base):
    __tablename__ = 'section'

    id = Column(INTEGER(11), primary_key=True)
    topicId = Column(ForeignKey('topic.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    name = Column(String(45), nullable=False)
    inactive = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    owner_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    weight = Column(INTEGER(11))

    owner = relationship('User')
    topic = relationship('Topic')


class HelpTopicStory(Base):
    __tablename__ = 'helpTopicStory'

    id = Column(INTEGER(11), primary_key=True)
    brand_id = Column(ForeignKey('brand.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    section_id = Column(ForeignKey('section.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    weight = Column(TINYINT(4), nullable=False, server_default=text("'0'"))

    brand = relationship('Brand')
    section = relationship('Section')
    story = relationship('Story')


class AssignmentUserTopicMapping(Base):
    __tablename__ = 'assignment_user_topic_mappings'

    id = Column(INTEGER(11), primary_key=True, comment='Primary Key')
    assignment_id = Column(ForeignKey('assignments.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                           index=True, comment='Assignment Id')
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True,
                     comment='User Id')
    topic_id = Column(ForeignKey('topic.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True,
                      comment='Topic Id')
    has_read = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='0=unread, 1=read')
    has_completed = Column(TINYINT(1), server_default=text("'0'"))
    updated_time = Column(DateTime)
    created_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='Created Time')
    flagPostProcess = Column(TINYINT(1), server_default=text("'0'"),
                             comment='0=Not processed, 1=processed, 2=under processing')
    flagNotifyCoaches = Column(TINYINT(1), server_default=text("'1'"), comment='0=no 1=yes')

    assignment = relationship('Assignment')
    topic = relationship('Topic')
    user = relationship('User')


class Workflow(Base):
    __tablename__ = 'workflow'

    id = Column(INTEGER(11), primary_key=True)
    workflowname = Column(String(50), nullable=False, server_default=text("''"))
    isdefault = Column(TINYINT(1), nullable=False, server_default=text("'0'"), comment='0=not default, 1=default')
    account_id = Column(ForeignKey('account.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    inactive = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    created_time = Column(DateTime)
    created_by = Column(ForeignKey('user.id'), index=True)
    lastmodified_time = Column(DateTime)
    lastmodified_by = Column(INTEGER(11))

    account = relationship('Account')
    user = relationship('User')


class Approval(Base):
    __tablename__ = 'approval'

    id = Column(INTEGER(11), primary_key=True)
    entity_type = Column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='1 = story 2 = guide')
    entity_id = Column(INTEGER(11), nullable=False, comment='(entity_type==1) : storyId ? guide')
    workflow_id = Column(ForeignKey('workflow.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    due_date = Column(DateTime, nullable=False)
    status = Column(TINYINT(1), nullable=False, server_default=text("'0'"),
                    comment='0 = not approved, 1 = approved, 2 = cancelled, 3 = paused, 4= resumed')
    created_time = Column(DateTime)
    created_by = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    lastmodified_time = Column(DateTime)
    lastmodified_by = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)

    user = relationship('User', primaryjoin='Approval.created_by == User.id')
    user1 = relationship('User', primaryjoin='Approval.lastmodified_by == User.id')
    workflow = relationship('Workflow')


class Brand(Base):
    __tablename__ = 'brand'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    enable_pwd_policy = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    inactive = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    audio_recorder = Column(INTEGER(4), server_default=text("'1'"), comment='1=Flash,2=HTML5,3=WOWZA')
    ui_section = Column(String(255), nullable=False, server_default=text("'Section'"))
    enable_screencast = Column(TINYINT(4), nullable=False, server_default=text("'1'"))
    enable_flash_recordings = Column(TINYINT(4), nullable=False, server_default=text("'1'"))
    ui_topic = Column(String(255), nullable=False, server_default=text("'Topic'"))
    video_analytics = Column(INTEGER(11), nullable=False, server_default=text("'0'"),
                             comment='`0` => video analytics disabled. `1` => video analytics enabled')
    screencast_over_http = Column(INTEGER(11), nullable=False, server_default=text("'0'"),
                                  comment='`0` means screencast will load over https. `1` means http')
    enable_surveys = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    enable_bot = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    bot_version = Column(String(255), server_default=text("'1.0'"), comment='Default is 1.0 and new is 1.1')
    luis_appId = Column(String(255))
    luis_subscription = Column(String(255))
    luis_reporting_subscription = Column(String(255))
    azure_subscription_id = Column(String(255))
    azure_resource_group = Column(String(255))
    azure_account_name = Column(String(255))
    azure_reporting_account = Column(String(255))
    msspeech_key = Column(String(255))
    msspeech_endpoint = Column(String(255), nullable=False, server_default=text("'westus'"))
    featured_content = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    webcam_recording = Column(TINYINT(4), nullable=False, server_default=text("'1'"),
                              comment='0 means disabled, 1 means enabled')
    preffered_browser = Column(INTEGER(11), nullable=False, server_default=text("'1'"),
                               comment="'1' => 'chrome', '2' => 'firefox', '3' => 'Safari', '4' => 'Internet Explorer'")
    browser_mode = Column(TINYINT(4), nullable=False, server_default=text("'0'"),
                          comment='0 means disabled, 1 means enabled')
    enable_fullstory = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    enable_terms = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    terms_text = Column(Text)
    admin_email = Column(String(55))
    logo = Column(String(255))
    bucket = Column(String(255), nullable=False, server_default=text("'caslon'"),
                    comment='S3 bucket assigned to a brand')
    ivr_number = Column(String(255), comment='Twilio number exposed to end user')
    recording_ivr_number = Column(String(255), comment='Twilio number exposed to end user to listen old recording')
    pipeline = Column(String(255), nullable=False, server_default=text("'1450075600383-q15ulu'"),
                      comment='Pipeline for elastic transcoder')
    url = Column(String(255), nullable=False, server_default=text("'app.zenarate.com'"))
    twilio_account_id = Column(String(255), comment='Twilio account id')
    twilio_account_token = Column(String(255), comment='Twilio account token')
    recording_preference = Column(TINYINT(1), nullable=False, server_default=text("'1'"),
                                  comment='1 = No Preference, 2 = VOIP, 3 = Telephony')
    profanity_filter = Column(String(255), nullable=False, server_default=text("'removed'"))
    profanity_library = Column(MEDIUMTEXT)
    enable_multifactor_authentication = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    created_by = Column(INTEGER(11), server_default=text("'0'"))
    user_workbench_version = Column(String(255), nullable=False, server_default=text("'v1'"),
                                    comment='Specifying versions of user workbench enabled for this brand')
    enable_practice_deletion = Column(TINYINT(4), server_default=text("'1'"), comment='0=disabled, 1=enabled')
    created_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), server_default=text("'0'"))
    last_updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    brand_setting = relationship('BrandSetting', primaryjoin='Brand.id == BrandSetting.brand_id')
    brand_telephony_setting = relationship('BrandTelephonySetting',
                                           primaryjoin='Brand.id == BrandTelephonySetting.brand_id')


class BrandSetting(Base):
    __tablename__ = 'brand_settings'

    id = Column(INTEGER(11), primary_key=True)
    brand_id = Column(ForeignKey('brand.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    settings_json = Column(LONGTEXT, nullable=False)
    inactive_settings = Column(TINYINT(4), server_default=text("'0'"))
    created_by = Column(INTEGER(11), nullable=False)
    created_time = Column(TIMESTAMP, nullable=False,
                          server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    brand = relationship('Brand')


class BrandTelephonySetting(Base):
    __tablename__ = 'brand_telephony_settings'

    id = Column(INTEGER(11), primary_key=True)
    brand_id = Column(ForeignKey('brand.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    ivr_number = Column(String(255), nullable=False, comment='Twilio number exposed to end user')
    type = Column(TINYINT(1), nullable=False, server_default=text("'1'"),
                  comment='1 = creating recording, 2 = Listening to recording')
    inactive = Column(TINYINT(1), server_default=text("'0'"))
    created_time = Column(DateTime)

    brand = relationship('Brand')


class BotUtterance(Base):
    __tablename__ = 'bot_user_utterance'

    id = Column(INTEGER(11), primary_key=True)
    brand_id = Column(INTEGER(11), nullable=False)
    utterance_id = Column(String(255), server_default=text("''"), comment='example id from LUIS')
    utterance_text = Column(MEDIUMTEXT, nullable=False, comment='example text')
    audio_clip = Column(String(255), nullable=False, server_default=text("''"), comment='audio clip name .mp3')
    clip_title = Column(String(255))
    filepath = Column(String(255))
    is_transcoded = Column(TINYINT(1), server_default=text("'0'"))
    duration = Column(INTEGER(11))
    inactive = Column(TINYINT(1), server_default=text("'0'"))
    type = Column(TINYINT(4), nullable=False, server_default=text("'1'"),
                  comment='1= user utterances, 2= bot responses')
    entity_id = Column(String(255), server_default=text("''"))
    start_char_index = Column(INTEGER(11), comment='starting index from where entity will be mapped in utterance text')
    end_char_index = Column(INTEGER(11), comment='ending index from where entity will be mapped in utterance text')
    created_by = Column(INTEGER(11), nullable=False)
    created_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), nullable=False)
    updated_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    response_tag_mappings = relationship('ResponseTagMapping',
                                         primaryjoin='ResponseTagMapping.bot_utterance_id == BotUtterance.id')


class Response(Base):
    __tablename__ = 'responses'

    id = Column(INTEGER(11), primary_key=True, unique=True)
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    # not used now
    script_id = Column(INTEGER(11), nullable=False, server_default=text("'1'"))
    # not used now
    intent_id = Column(String(255))
    intent = Column(String(255))
    bot_utterance_id = Column(ForeignKey('bot_user_utterance.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    parent_id = Column(INTEGER(11))
    sequence = Column(TINYINT(4), server_default=text("'1'"), comment='sequence order in call flow')
    type = Column(TINYINT(1), nullable=False, server_default=text("'1'"),
                  comment='0=opening statement, 1=Customer response, 2= last statement')
    created_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(INTEGER(11))
    updated_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11))

    story = relationship('Story')
    # coach = relationship('User', primaryjoin='Account.coach_id == User.id')
    botUtterance = relationship('BotUtterance', primaryjoin='Response.bot_utterance_id == BotUtterance.id')


class AudiobotPracticeSession(Base):
    __tablename__ = 'audiobot_practice_session'

    id = Column(INTEGER(11), primary_key=True)
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    video_id = Column(ForeignKey('video.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    bot_response_id = Column(ForeignKey('responses.id', ondelete='CASCADE', onupdate='CASCADE'), index=True,
                             nullable=True)
    bot_response_text = Column(Text)
    agent_response_text = Column(Text, nullable=False)
    weight = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    bot_audio_clip = Column(String(255))
    audio_clip = Column(String(255))
    created_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    isUploaded = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    isEncoded = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    isReviewed = Column(TINYINT(4), nullable=False, server_default=text("'1'"))

    story = relationship('Story')
    user = relationship('User')
    video = relationship('Video')
    response = relationship('Response')


class StoryGuideMapping(Base):
    __tablename__ = 'story_guide_mappings'

    id = Column(INTEGER(11), primary_key=True, comment='Story Guide Mapping Id')
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True,
                      comment='Story Id')
    guide_id = Column(ForeignKey('video.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True,
                      comment='Guide Id')
    owner_id = Column(INTEGER(11), nullable=False, comment='Owner Id')
    owner_account_id = Column(INTEGER(11), nullable=False, comment='Owner Acount Id')
    guide_context = Column(TINYINT(1), server_default=text("'1'"),
                           comment="'1'=>'Guide','2'=>'Context','3'=>'Question'")
    created_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"), comment='Created Time')
    isapproved = Column(TINYINT(1), server_default=text("'0'"), comment='0 = not approved, 1= approved')
    ispromoted = Column(TINYINT(1), server_default=text("'0'"), comment='0 = not promoted, 1 = promoted')

    guide = relationship('Video')
    story = relationship('Story')


class StoryAccountMapping(Base):
    __tablename__ = 'storyAccountMapping'

    id = Column(INTEGER(11), primary_key=True)
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    account_id = Column(ForeignKey('account.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    weight = Column(INTEGER(11))
    completelyAssigned = Column(TINYINT(4))
    created_time = Column(DateTime)
    owner_account_id = Column(ForeignKey('account.id', ondelete='CASCADE', onupdate='CASCADE'), index=True,
                              comment='Account Id of owner while creating story\\n ')

    account = relationship('Account', primaryjoin='StoryAccountMapping.account_id == Account.id')
    owner_account = relationship('Account', primaryjoin='StoryAccountMapping.owner_account_id == Account.id')
    story = relationship('Story')


class HashcodeMapping(Base):
    __tablename__ = 'hashcode_mappings'

    id = Column(INTEGER(11), primary_key=True)
    brand_id = Column(INTEGER(11), nullable=False)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    video_id = Column(INTEGER(11))
    assignment_id = Column(INTEGER(11))
    hashcode = Column(String(20), comment='combination of rowId, userId, storyId')
    call_id = Column(String(100), comment='call id of twilio call')
    authenticated = Column(TINYINT(11), nullable=False, server_default=text("'0'"),
                           comment='if user pass the authentication, it will switch to 1, default is 0')
    recording_id = Column(String(100), comment='recording id on Twilio account')
    video_type = Column(TINYINT(1), nullable=False, server_default=text("'1'"),
                        comment='1 = Practise, 2 = ScreenCast, 3 = Uploads, 4 = AudioOnly, 5 = InteractiveAudio')
    isReadonly = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    created_time = Column(TIMESTAMP)

    story = relationship('Story')
    user = relationship('User')


class Share(Base):
    __tablename__ = 'share'

    id = Column(INTEGER(11), primary_key=True)
    video_id = Column(ForeignKey('video.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    assignment_id = Column(INTEGER(11))
    sharedWith = Column(INTEGER(11), index=True,
                        comment="group_id, manager(of user's account), user's account_id, user id (when shared video within account)")
    sharedBy = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    type = Column(INTEGER(11), comment='0=account, 1= manager, 2= group, 3=individual people')
    shareType = Column(CHAR(1), nullable=False, server_default=text("'S'"), comment='S=Story, T=topic')
    created_time = Column(DateTime)

    user = relationship('User')
    story = relationship('Story')
    video = relationship('Video')
    sharedWithUser = relationship('User')
    sharedByUser = relationship('User')


class AuthItem(Base):
    __tablename__ = 'AuthItem'

    name = Column(String(64), primary_key=True)
    type = Column(INTEGER(11), nullable=False)
    description = Column(Text)
    bizrule = Column(Text)
    data = Column(Text)


class AuthItemChild(Base):
    __tablename__ = 'AuthItemChild'

    parent = Column('parent', ForeignKey('AuthItem.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True,
                    nullable=False)
    child = Column('child', ForeignKey('AuthItem.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True,
                   nullable=False, index=True)

    auth_parent = relationship('AuthItem', primaryjoin='AuthItemChild.parent == AuthItem.name')
    auth_child = relationship('AuthItem', primaryjoin='AuthItemChild.child == AuthItem.name')


class AuthAssignment(Base):
    __tablename__ = 'AuthAssignment'

    itemname = Column(ForeignKey('AuthItem.name', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True,
                      nullable=False)
    userid = Column('userid', ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    # userid = Column(String(64), primary_key=True, nullable=False)
    bizrule = Column(Text)
    data = Column(Text)

    authitem = relationship('AuthItem')
    user = relationship('User')


class UserVideoAnalytic(Base):
    __tablename__ = 'user_video_analytics'

    id = Column(INTEGER(11), primary_key=True)
    account_id = Column(ForeignKey('account.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    assignment_id = Column(ForeignKey('assignments.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                           index=True)
    ausm_autm = Column(String(255), server_default=text("''"), comment='S=ausm, T=autm')
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    video_id = Column(ForeignKey('video.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    viewed = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    view_start_date = Column(DateTime)
    last_viewed_date = Column(DateTime)
    flag_compute = Column(TINYINT(4), nullable=False, server_default=text("'0'"),
                          comment='0 = no activity, 1= recent activity done')

    account = relationship('Account')
    assignment = relationship('Assignment')
    story = relationship('Story')
    user = relationship('User')
    video = relationship('Video')


class DraftComment(Base):
    __tablename__ = 'draft_comments'

    id = Column(INTEGER(11), primary_key=True)
    video_id = Column(ForeignKey('video.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    comments = Column(Text, nullable=False)
    created_time = Column(DateTime)
    updated_time = Column(DateTime)

    user = relationship('User')
    video = relationship('Video')


class UserOtherCoach(Base):
    __tablename__ = 'user_other_coaches'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    coach_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    coach = relationship('User', primaryjoin='UserOtherCoach.coach_id == User.id')
    user = relationship('User', primaryjoin='UserOtherCoach.user_id == User.id')


class TagCollection(Base):
    __tablename__ = 'tag_collections'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    account_id = Column(ForeignKey('account.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    created_by = Column(ForeignKey('user.id', onupdate='CASCADE'), index=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    entity = Column(TINYINT(1), nullable=False, server_default=text("'1'"),
                    comment='1= user, 2 = story, 3 = bot-response')

    account = relationship('Account')
    tag = relationship('Tag')
    user = relationship('User')


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    bg_color = Column(String(255), nullable=False)
    account_id = Column(ForeignKey('account.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    tag_collection_id = Column(ForeignKey('tag_collections.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                               index=True)
    created_by = Column(ForeignKey('user.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    account = relationship('Account')
    user = relationship('User')
    tag_collection = relationship('TagCollection')


class UserTagMapping(Base):
    __tablename__ = 'user_tag_mappings'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    tag_id = Column(ForeignKey('tags.id'), nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    tag = relationship('Tag')
    user = relationship('User')


class InviteUser(Base):
    __tablename__ = 'inviteUsers'

    id = Column(INTEGER(11), primary_key=True)
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    invitedUser = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    created_time = Column(DateTime)

    user = relationship('User')
    story = relationship('Story')


class StoryRule(Base):
    __tablename__ = 'story_rule'

    id = Column(INTEGER(11), primary_key=True)
    brand_id = Column(INTEGER(11), nullable=False)
    story_id = Column(INTEGER(11), nullable=False)
    name = Column(String(45), server_default=text("'0'"))
    story_json = Column(LONGTEXT, nullable=False)
    is_draft = Column(TINYINT(4), server_default=text("'0'"))
    type = Column(TINYINT(4), server_default=text("'0'"), comment='0= Staging, 1= Production, 2=Restore Point')
    warn_overwriting = Column(TINYINT(4), server_default=text("'0'"))
    created_by = Column(INTEGER(11), nullable=False)
    created_datetime = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), nullable=False)
    updated_datetime = Column(TIMESTAMP, nullable=False,
                              server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class CallScore(Base):
    __tablename__ = 'call_scores'

    id = Column(INTEGER(11), primary_key=True)
    video_id = Column(ForeignKey('video.id', ondelete='CASCADE'), nullable=False, index=True)
    coach_id = Column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)
    score_json = Column(LONGTEXT, nullable=False)
    is_draft = Column(TINYINT(4), server_default=text("'0'"))
    inactive = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    created_datetime = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey('user.id', ondelete='CASCADE'), nullable=False, index=True)

    coach = relationship('User', primaryjoin='CallScore.coach_id == User.id')
    user = relationship('User', primaryjoin='CallScore.created_by == User.id')
    video = relationship('Video')


'''	 Analytics DB. '''


class AuditsPython(Base):
    __tablename__ = 'audits_python'
    __bind_key__ = 'analytics'

    id = Column(INTEGER(11), primary_key=True)
    event_type = Column(String(255), comment='type of the event to be audited')
    event_id = Column(String(255), comment='referenced tables primary key')
    user_id = Column(INTEGER(11), comment='id of user who is performing the event')
    session_id = Column(String(255), comment='session id of the user to track a particular session')
    brandName = Column(INTEGER(11))
    user_email = Column(String(255), comment='email of user who is performing the event')
    user_name = Column(String(255))
    data = Column(Text, comment='Additional data for the event')
    ip_address = Column(String(255), comment='ip address of the user')
    server_name = Column(String(255), comment='domain on which the event is being created')
    request_uri = Column(Text, comment='request URI parameters')
    user_agent = Column(Text, comment='User Agent Details')
    created_date = Column(DateTime, nullable=False, comment='date created')


class BlacklistedToken(Base):
    __tablename__ = 'blacklisted_tokens'

    id = Column(INTEGER(11), primary_key=True)
    token = Column(String(255))
    token_type = Column(TINYINT(1), server_default=text("'1'"))
    inactive = Column(TINYINT(1), server_default=text("'0'"))


class ResponseTagMapping(Base):
    __tablename__ = 'response_tag_mappings'

    id = Column(INTEGER(11), primary_key=True)
    bot_utterance_id = Column(ForeignKey('bot_user_utterance.id', ondelete='CASCADE'), nullable=False, index=True)
    tag_id = Column(ForeignKey('tags.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    bot_utterance = relationship('BotUtterance')
    tag = relationship('Tag')


class StoryCallFlow(Base):
    __tablename__ = 'story_call_flow'

    id = Column(INTEGER(11), primary_key=True)
    brand_id = Column(INTEGER(11), nullable=False)
    story_rule_id = Column(INTEGER(11), nullable=False)
    story_id = Column(INTEGER(11), nullable=False)
    call_json = Column(LONGTEXT, nullable=False)
    call_configuration = Column(LONGTEXT, nullable=False)
    is_draft = Column(TINYINT(4), server_default=text("'0'"))
    created_by = Column(INTEGER(11), nullable=False)
    created_datetime = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), nullable=False)
    updated_datetime = Column(TIMESTAMP, nullable=False,
                              server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


'''	 Coach DB. '''


class CallCategory(Base):
    __tablename__ = 'call_category'
    __bind_key__ = 'coach'

    id = Column(INTEGER(11), primary_key=True)
    call_category = Column(String(255))
    description = Column(LONGTEXT)
    created_by = Column(INTEGER(11))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), server_default=text("'0'"))
    updated_at = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    inactive = Column(TINYINT(1), server_default=text("'0'"))


class CallDetails(Base):
    __tablename__ = 'call_details'
    __bind_key__ = 'coach'

    id = Column(INTEGER(11), primary_key=True)
    call_id = Column(INTEGER(11))
    call_direction = Column(String(255))
    call_base_path = Column(LONGTEXT)
    call_identifier = Column(String(255))
    call_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    call_supervisor_id = Column(INTEGER(11))
    call_manager = Column(INTEGER(11))
    call_agent = Column(INTEGER(11))
    call_processing_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    model_id = Column(INTEGER(11))
    brand_id = Column(INTEGER(11))
    created_by = Column(INTEGER(11))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), server_default=text("'0'"))
    updated_at = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    inactive = Column(TINYINT(1), server_default=text("'0'"))


class CallScorecards(Base):
    __tablename__ = 'call_scorecards'
    __bind_key__ = 'coach'

    id = Column(INTEGER(11), primary_key=True)
    call_id = Column(INTEGER(11))
    scorecard_path = Column(LONGTEXT)
    model_id = Column(INTEGER(11))
    brand_id = Column(ForeignKey('brand.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    created_by = Column(INTEGER(11))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), server_default=text("'0'"))
    updated_at = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    inactive = Column(TINYINT(1), server_default=text("'0'"))


class EntitiesLibrary(Base):
    __tablename__ = 'entities_library'
    __bind_key__ = 'coach'

    id = Column(INTEGER(11), primary_key=True)
    call_category_id = Column(ForeignKey('call_category.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    entity = Column(String(255))
    created_by = Column(INTEGER(11))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), server_default=text("'0'"))
    updated_at = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    inactive = Column(TINYINT(1), server_default=text("'0'"))


class IntentsLibrary(Base):
    __tablename__ = 'intents_library'
    __bind_key__ = 'coach'

    id = Column(INTEGER(11), primary_key=True)
    call_category_id = Column(ForeignKey('call_category.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    intent = Column(String(255))
    created_by = Column(INTEGER(11))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), server_default=text("'0'"))
    updated_at = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    inactive = Column(TINYINT(1), server_default=text("'0'"))



class RuleAlgorithms(Base):
    __tablename__ = 'rule_algorithms'
    __bind_key__ = 'coach'

    id = Column(INTEGER(11), primary_key=True)
    algo_name = Column(String(255))
    configuration_parameters = Column(LONGTEXT)
    version = Column(String(255))
    description = Column(LONGTEXT)
    created_by = Column(INTEGER(11))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), server_default=text("'0'"))
    updated_at = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    inactive = Column(TINYINT(1), server_default=text("'0'"))


class TrainingModels(Base):
    __tablename__ = 'training_models'
    __bind_key__ = 'coach'

    id = Column(INTEGER(11), primary_key=True)
    model_name = Column(String(255))
    algorithm_id = Column(ForeignKey('rule_algorithms.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    description = Column(LONGTEXT)
    model_path = Column(LONGTEXT)
    production_model_compiled_path = Column(LONGTEXT)
    staging_model_compiled_path = Column(LONGTEXT)
    version = Column(String(255))
    brand_id = Column(ForeignKey('brand.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    staging_published_date = Column(DateTime)
    production_published_date = Column(DateTime)
    created_by = Column(INTEGER(11))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), server_default=text("'0'"))
    updated_at = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    inactive = Column(TINYINT(1), server_default=text("'0'"))


class TrainingRequests(Base):
    __tablename__ = 'training_requests'
    __bind_key__ = 'coach'

    id = Column(INTEGER(11), primary_key=True)
    item_name = Column(String(255))
    item_type = Column(String(255))
    call_category_id = Column(ForeignKey('call_category.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    requested_by = Column(INTEGER(11))
    brand_id = Column(ForeignKey('brand.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    status = Column(TINYINT(1), server_default=text("'0'"))
    requested_date = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    decision_by = Column(INTEGER(11))
    decision_date = Column(DateTime)
    created_by = Column(INTEGER(11))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), server_default=text("'0'"))
    updated_at = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    inactive = Column(TINYINT(1), server_default=text("'0'"))


class UtteranceEntitiesMapping(Base):
    __tablename__ = 'utterance_entities_mapping'
    __bind_key__ = 'coach'

    id = Column(INTEGER(11), primary_key=True)
    uim_id = Column(ForeignKey('utterances_intents_mapping.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    call_id = Column(String(255))
    entity_id = Column(INTEGER(11))
    startIndex = Column(INTEGER(11))
    endIndex = Column(INTEGER(11))
    brand_id = Column(ForeignKey('brand.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    created_by = Column(INTEGER(11))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), server_default=text("'0'"))
    updated_at = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    inactive = Column(TINYINT(1), server_default=text("'0'"))


class UtterancesIntentsMapping(Base):
    __tablename__ = 'utterances_intents_mapping'
    __bind_key__ = 'coach'

    id = Column(INTEGER(11), primary_key=True)
    intent_id = Column(ForeignKey('intents_library.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    utterance_text = Column(LONGTEXT)
    utterance_id = Column(INTEGER(11))
    call_id = Column(String(255))
    startTimeOffset = Column(String(255))
    durationTimeOffset = Column(String(255))
    brand_id = Column(ForeignKey('brand.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    created_by = Column(INTEGER(11))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), server_default=text("'0'"))
    updated_at = Column(TIMESTAMP, nullable=True, server_default=text("CURRENT_TIMESTAMP"))
    inactive = Column(TINYINT(1), server_default=text("'0'"))


class CallAnalyzerConfiguration(Base):
    __tablename__ = 'call_analyzer_configuration'
    __bind_key__ = 'coach'

    id = Column(INTEGER(11), primary_key=True)
    configuration_type = Column(String(255), nullable=False)
    configuration_value = Column(String(255), nullable=False)
    extra_parameter = Column(LONGTEXT, nullable=False)
    brand_id = Column(INTEGER(11), nullable=False)
    inactive = Column(TINYINT(1), server_default=text("'0'"))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(INTEGER(11))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_by = Column(INTEGER(11), server_default=text("'0'"))


class Timezone(Base):
    __tablename__ = 'timezone'

    id = Column(INTEGER(11), primary_key=True)
    dst_id = Column(INTEGER(11))
    code = Column(String(8), nullable=False)
    name = Column(String(255), nullable=False)
    code_name = Column(String(255), nullable=False)
    gmt_code = Column(String(32), nullable=False)
    offset_sec = Column(String(8), nullable=False, server_default=text("''"))
    offset = Column(Float, nullable=False)
    created_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    inactive = Column(TINYINT(1), nullable=False, server_default=text("'0'"))


class AssignmentUserMapping(Base):
    __tablename__ = 'assignment_user_mappings'

    id = Column(INTEGER(11), primary_key=True, comment='Primary Key')
    assignment_id = Column(ForeignKey('assignments.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                           index=True, comment='Assignment Id')
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True,
                     comment='User Id')
    disable_reminder_flag = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    created_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='Created on')

    assignment = relationship('Assignment')
    user = relationship('User')


class Favorite(Base):
    __tablename__ = 'favorites'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    element_id = Column(INTEGER(11), nullable=False)
    element_type = Column(String(1), nullable=False, server_default=text("''"),
                          comment='T = topic, S = story, R = recording')
    created_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')


class SupportTicket(Base):
    __tablename__ = 'support_ticket'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False, comment='User Id')
    brand_id = Column(INTEGER(11), nullable=False)
    phone = Column(String(30), nullable=False)
    issue_desc = Column(LONGTEXT, nullable=False)
    issue_title = Column(String(255))
    created_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='Created on')
    s3_file_path = Column(String(255))


class TopicAccountMapping(Base):
    __tablename__ = 'topicAccountMapping'

    id = Column(INTEGER(11), primary_key=True)
    account_id = Column(ForeignKey('account.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    topic_id = Column(ForeignKey('topic.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    weight = Column(INTEGER(11), nullable=False, server_default=text("'0'"))

    account = relationship('Account')
    topic = relationship('Topic')


class SubSection(Base):
    __tablename__ = 'SubSection'

    id = Column(INTEGER(11), primary_key=True)
    topicId = Column(ForeignKey('topic.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    sectionId = Column(INTEGER(11), nullable=False)
    owner_id = Column(INTEGER(11), nullable=False, comment='Owner Id')
    name = Column(String(45), nullable=False)
    inactive = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    weight = Column(INTEGER(11))
    created_byCopy = Column(INTEGER(11))


class StorySectionMapping(Base):
    __tablename__ = 'storySectionMapping'

    id = Column(INTEGER(11), primary_key=True)
    story_id = Column(ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    sectionId = Column(ForeignKey('section.id'), nullable=False, index=True)
    topicAccountMappingId = Column(ForeignKey('topicAccountMapping.id', ondelete='CASCADE', onupdate='CASCADE'),
                                   index=True)
    weight = Column(INTEGER(11), nullable=False, server_default=text("'0'"),
                    comment='Weight field to order stories inside section')
    subSectionId = Column(INTEGER(11))

    section = relationship('Section')
    story = relationship('Story')
